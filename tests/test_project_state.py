"""Isolated project-state lifecycle tests; keep failure evidence in private work."""

from datetime import date
import copy
import json
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
WORK = ROOT / ".checkpoint-karpathy/private/work/verification/project-state"
spec = importlib.util.spec_from_file_location("project_state", ROOT / "scripts/project_state.py")
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class ProjectStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        WORK.mkdir(parents=True, exist_ok=True)
        cls.run_root = Path(tempfile.mkdtemp(prefix="run-", dir=WORK))
        print(f"Project-state test evidence: {cls.run_root}", flush=True)

    def setUp(self):
        self.project = self.run_root / self._testMethodName / "项目 with spaces"
        self.project.mkdir(parents=True)
        self.base = self.project / ".checkpoint-karpathy"

    def invoke(self, command, *args, success=True, payload=None):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / command), "--project", str(self.project), *args],
            capture_output=True, text=True, timeout=15,
            input=json.dumps(payload, ensure_ascii=False) if payload is not None else "",
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def snapshot(self, path):
        return {str(p.relative_to(path)): p.read_bytes() for p in path.rglob("*") if p.is_file()}

    def initialize(self, mode="collaborative", goal=True):
        self.invoke("init_project.py", "--mode", mode)
        folder = self.base / "private" if mode == "privacy" else self.base
        if goal:
            self.invoke("create_goal.py", payload=self.payload())
        return folder, folder / "roadmap"

    def payload(self):
        return {
            "language": "zh", "goal": "实现用户目标", "acceptance": ["真实行为通过项目验收"],
            "included": ["相关实现和验证"], "non_goals": [], "work_mode": "feature",
            "initial_state": "功能尚不存在", "current_state": "待开发", "next_action": "执行 1.1",
            "context": {"constraints": ["保留既有行为"], "assumptions": [], "risks": [], "blockers": []},
            "milestones": [{"id": "1", "title": "交付功能", "purpose": "达成完整目标", "dependencies": [],
                "phases": [{"id": "1.1", "title": "实现功能", "dependencies": [], "scope": "实际需求",
                    "success_criteria": "实现可观察行为", "verification": "项目定向测试",
                    "commit": "feat(core): implement requested behavior"}],
                "review": {"verification": "完整相关回归", "commit": "chore(review): review feature"}}],
        }

    def terminal(self, roadmap, value="completed"):
        (roadmap / "status.md").write_text(f"# 状态\n\n## Completion\n{value}\n\n## Current State\n已结束\n", encoding="utf-8")

    def test_initialization_modes_defaults_and_private_ignore(self):
        (self.project / ".gitignore").write_text("existing-rule")
        self.invoke("init_project.py", "--mode", "privacy", "--language", "zh", "--commit-message-style", "phase")
        config = self.base / "private/config.yaml"
        self.assertEqual(yaml.safe_load(config.read_text()), {"mode": "privacy", "commit_message_style": "phase"})
        self.assertIn("默认", config.read_text())
        self.assertIn("conventional", config.read_text())
        self.assertTrue((self.base / "private/work").is_dir())
        self.assertFalse((self.base / "archive").exists())
        self.assertFalse((self.base / "config.yaml").exists())
        self.assertEqual((self.project / ".gitignore").read_text(), "existing-rule\n.checkpoint-karpathy/private/\n")
        self.assertEqual(list((config.parent / "roadmap").iterdir()), [])

    def test_repeat_initialization_preserves_user_content_and_configuration(self):
        folder, roadmap = self.initialize()
        config = folder / "config.yaml"
        config.write_text(config.read_text() + "\n# local note\n")
        (roadmap / "README.md").write_text("用户实际目标\n", encoding="utf-8")
        (roadmap / "custom.md").write_text("extra")
        before = self.snapshot(self.project)
        self.invoke("init_project.py", "--mode", "collaborative", "--language", "zh")
        self.assertEqual(self.snapshot(self.project), before)
        self.assertEqual(yaml.safe_load(config.read_text())["commit_message_style"], "conventional")
        self.invoke("init_project.py", "--mode", "privacy", success=False)
        self.invoke("init_project.py", "--mode", "collaborative", "--commit-message-style", "phase", success=False)
        self.assertEqual(self.snapshot(self.project), before)

    def test_private_ignore_survives_later_exception_rules(self):
        subprocess.run(["git", "init", "--quiet", str(self.project)], check=True)
        ignore = self.project / ".gitignore"
        original = ".checkpoint-karpathy/private/\n!.checkpoint-karpathy/private/\n"
        ignore.write_text(original)
        folder, roadmap = self.initialize("privacy")
        for path in (folder / "config.yaml", roadmap / "README.md", folder / "work/evidence.log"):
            result = subprocess.run(["git", "-C", str(self.project), "check-ignore", "--no-index", str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(ignore.read_text().startswith(original))
        before = self.snapshot(self.project)
        self.invoke("init_project.py", "--mode", "privacy")
        self.assertEqual(self.snapshot(self.project), before)

    def test_existing_complete_goal_without_config_is_preserved(self):
        roadmap = self.base / "roadmap"
        roadmap.mkdir(parents=True)
        for name in state.DOCUMENTS:
            (roadmap / name).write_text("existing " + name)
        before = self.snapshot(roadmap)
        self.invoke("init_project.py", "--mode", "collaborative")
        self.assertEqual(self.snapshot(roadmap), before)
        self.assertTrue((self.base / "config.yaml").is_file())

    def test_partial_state_and_opposite_mode_content_are_not_overwritten(self):
        roadmap = self.base / "roadmap"
        roadmap.mkdir(parents=True)
        (roadmap / "README.md").write_text("recover this goal")
        before = self.snapshot(self.project)
        self.invoke("init_project.py", "--mode", "collaborative", success=False)
        self.invoke("init_project.py", "--mode", "privacy", success=False)
        self.assertEqual(self.snapshot(self.project), before)

    def test_conflicting_and_invalid_yaml_stops_without_changing_state(self):
        folder, _ = self.initialize()
        config = folder / "config.yaml"
        variants = (
            "mode: collaborative\nmode: privacy\ncommit_message_style: conventional\n",
            "mode: collaborative\n",
            "mode: invalid\ncommit_message_style: conventional\n",
            "mode: privacy\ncommit_message_style: conventional\n",
            "mode: [\n",
            "mode: collaborative\ncommit_message_style: conventional\nextra: value\n",
        )
        for content in variants:
            with self.subTest(content=content):
                config.write_text(content)
                before = self.snapshot(self.project)
                self.invoke("archive_goal.py", "--title", "old-goal", success=False)
                self.assertEqual(self.snapshot(self.project), before)
        config.write_text(state.config_text("collaborative", "conventional", "en"))
        (self.base / "private/config.yaml").write_text(state.config_text("privacy", "phase", "en"))
        before = self.snapshot(self.project)
        self.invoke("init_project.py", "--mode", "collaborative", success=False)
        self.invoke("archive_goal.py", "--title", "old-goal", success=False)
        self.assertEqual(self.snapshot(self.project), before)

    def test_archive_both_modes_includes_hidden_and_nested_files(self):
        for mode, terminal in (("collaborative", "completed"), ("privacy", "cancelled")):
            with self.subTest(mode=mode):
                project = self.project / mode
                project.mkdir()
                roadmap = state.initialize(project, mode)
                state.create(project, self.payload())
                self.terminal(roadmap, terminal)
                (roadmap / ".hidden").write_text("hidden evidence")
                (roadmap / "design").mkdir()
                (roadmap / "design/history.md").write_text("custom history")
                work = project / ".checkpoint-karpathy/private/work"
                (work / "logs").mkdir()
                (work / "logs/result.txt").write_text("retain work")
                old_goal = self.snapshot(roadmap)
                old_work = self.snapshot(work)
                inode = roadmap.stat().st_ino
                config = (roadmap.parent / "config.yaml").read_bytes()
                destination, active = state.archive(project, "旧目标-summary")
                self.assertEqual(destination.parent, roadmap.parent / "archive")
                self.assertEqual(self.snapshot(destination), old_goal)
                self.assertFalse((destination / "roadmap").exists())
                self.assertEqual(active, roadmap)
                self.assertEqual(roadmap.stat().st_ino, inode)
                self.assertEqual(list(roadmap.iterdir()), [])
                self.assertEqual((roadmap.parent / "config.yaml").read_bytes(), config)
                self.assertEqual(self.snapshot(work), old_work)
                state.create(project, self.payload())
                self.assertIn("\nincomplete\n", (roadmap / "status.md").read_text())

    def test_archive_rejects_active_unclear_status_and_invalid_titles(self):
        _, roadmap = self.initialize()
        for value in ("incomplete", "paused", "completed maybe"):
            self.terminal(roadmap, value)
            before = self.snapshot(self.project)
            self.invoke("archive_goal.py", "--title", "old-goal", success=False)
            self.assertEqual(self.snapshot(self.project), before)
        (roadmap / "status.md").write_text("## 自定义状态\n已完成\n")
        result = self.invoke("archive_goal.py", "--title", "old-goal", success=False)
        self.assertIn("reconcile", result.stderr)
        self.terminal(roadmap)
        for title in ("../escape", "a/b", "", "a\\b", "a b", "-bad", "bad-"):
            before = self.snapshot(self.project)
            self.invoke("archive_goal.py", "--title", title, success=False)
            self.assertEqual(self.snapshot(self.project), before)

    def test_archive_date_suffix_rollover_preserves_existing_archives(self):
        folder, roadmap = self.initialize()
        archive = folder / "archive"
        archive.mkdir()
        for index in range(1, 27):
            (archive / f"{date.today():%Y%m%d}{state.suffix(index)}-old-goal").mkdir()
        self.terminal(roadmap)
        self.invoke("archive_goal.py", "--title", "old-goal")
        self.assertTrue((archive / f"{date.today():%Y%m%d}aa-old-goal/status.md").is_file())
        self.assertEqual(len(list(archive.iterdir())), 27)
        self.invoke("create_goal.py", payload=self.payload())
        self.terminal(roadmap, "cancelled")
        self.invoke("archive_goal.py", "--title", "different-goal")
        self.assertTrue((archive / f"{date.today():%Y%m%d}ab-different-goal/status.md").is_file())

    def test_archive_failure_restores_old_goal(self):
        _, roadmap = self.initialize()
        self.terminal(roadmap)
        (roadmap / "custom").mkdir()
        (roadmap / "custom/evidence").write_text("preserve")
        original = self.snapshot(roadmap)
        original_move = state.move
        calls = 0

        def failing_move(source, destination):
            nonlocal calls
            if source.parent == roadmap:
                calls += 1
                if calls == 3:
                    raise OSError("injected move failure")
            original_move(source, destination)

        with patch.object(state, "move", side_effect=failing_move):
            with self.assertRaisesRegex(state.StateError, "original goal restored"):
                state.archive(self.project, "old-goal")
        self.assertEqual(self.snapshot(roadmap), original)
        self.assertEqual(list((roadmap.parent / "archive").iterdir()), [])

    def test_archive_recovery_failure_reports_paths_and_preserves_content(self):
        _, roadmap = self.initialize()
        self.terminal(roadmap)
        original = self.snapshot(roadmap)
        original_move = state.move
        calls = 0

        def failing_move(source, destination):
            nonlocal calls
            calls += 1
            if calls >= 2:
                raise OSError("move and recovery failure")
            original_move(source, destination)

        with patch.object(state, "move", side_effect=failing_move):
            with self.assertRaisesRegex(state.StateError, "recovery also failed.*roadmap.*archive"):
                state.archive(self.project, "old-goal")
        archived = next((roadmap.parent / "archive").iterdir())
        retained = self.snapshot(roadmap)
        retained.update(self.snapshot(archived))
        self.assertEqual(retained, original)

    def test_creation_rejects_conflicting_opposite_mode_content(self):
        self.initialize(goal=False)
        other = self.base / "private/roadmap"
        other.mkdir()
        (other / "notes.md").write_text("preserve")
        before = self.snapshot(self.project)
        for arguments in ((), ("--check-only",)):
            result = self.invoke("create_goal.py", *arguments, payload=self.payload(), success=False)
            self.assertIn("outside the selected mode", result.stderr)
            self.assertEqual(self.snapshot(self.project), before)

    def test_creation_failure_restores_empty_roadmap_and_retains_rendered_content(self):
        _, roadmap = self.initialize(goal=False)
        original_move = state.move
        calls = 0

        def failing_move(source, destination):
            nonlocal calls
            if source.parent.name.startswith("goal-"):
                calls += 1
                if calls == 3:
                    raise OSError("activation failure")
            original_move(source, destination)

        with patch.object(state, "move", side_effect=failing_move):
            with self.assertRaisesRegex(state.StateError, "restored to staging"):
                state.create(self.project, self.payload())
        self.assertEqual(list(roadmap.iterdir()), [])
        prepared = next((self.base / "private/work/staging").iterdir())
        self.assertEqual(set(self.snapshot(prepared)), set(state.DOCUMENTS))
        self.assertIn("实现用户目标", (prepared / "README.md").read_text())
        self.invoke("create_goal.py", payload=self.payload())

    def test_rollback_failure_reports_paths_and_retains_all_content(self):
        _, roadmap = self.initialize(goal=False)
        original_move = state.move
        activation = 0

        def failing_move(source, destination):
            nonlocal activation
            if source.parent.name.startswith("goal-"):
                activation += 1
                if activation == 2:
                    raise OSError("activation failure")
            if source.parent == roadmap:
                raise OSError("restoration failure")
            original_move(source, destination)

        with patch.object(state, "move", side_effect=failing_move):
            with self.assertRaisesRegex(state.StateError, "recovery also failed.*staging"):
                state.create(self.project, self.payload())
        prepared = next((self.base / "private/work/staging").iterdir())
        self.assertEqual(set(self.snapshot(prepared)) | set(self.snapshot(roadmap)), set(state.DOCUMENTS))

    def test_missing_template_and_state_symlink_do_not_move_old_goal(self):
        fresh_project = self.project / "fresh"
        fresh_project.mkdir()
        with patch.object(state, "PACKAGE", self.project / "missing-package"):
            with self.assertRaises(OSError):
                state.initialize(fresh_project, "privacy")
        self.assertEqual(list(fresh_project.iterdir()), [])
        _, roadmap = self.initialize(goal=False)
        before = self.snapshot(self.project)
        with patch.object(state, "PACKAGE", self.project / "missing-package"):
            with self.assertRaises(OSError):
                state.create(self.project, self.payload())
        self.assertEqual(self.snapshot(self.project), before)
        self.invoke("create_goal.py", payload=self.payload())
        self.terminal(roadmap)
        external = self.project / "external-archive"
        external.mkdir()
        (roadmap.parent / "archive").symlink_to(external, target_is_directory=True)
        self.invoke("archive_goal.py", "--title", "old-goal", success=False)
        self.assertEqual(list(external.iterdir()), [])

    def test_structured_creation_long_unicode_content_and_initial_records(self):
        _, roadmap = self.initialize(goal=False)
        payload = self.payload()
        long_scope = "中文 $HOME `literal` 多行说明\n" * 15000
        payload["milestones"][0]["phases"][0]["scope"] = long_scope
        self.invoke("create_goal.py", payload=payload)
        self.assertEqual(set(self.snapshot(roadmap)), set(state.DOCUMENTS))
        plan = (roadmap / "milestones.md").read_text()
        self.assertIn("中文 $HOME `literal`", plan)
        self.assertIn("- [ ] 1.1", plan)
        self.assertIn("- [ ] Milestone 1 Review", plan)
        self.assertNotIn("[x]", plan)
        self.assertNotIn("<!--", plan)
        self.assertIn("incomplete", (roadmap / "status.md").read_text())
        self.assertIn("生成线路图", (roadmap / "progress.md").read_text())
        self.assertIn("未执行项目测试", (roadmap / "progress.md").read_text())
        self.assertIn("建立初始计划", (roadmap / "changelog.md").read_text())
        self.assertNotIn("config.yaml", (roadmap / "progress.md").read_text())
        before = self.snapshot(self.project)
        self.invoke("create_goal.py", payload=payload, success=False)
        self.assertEqual(self.snapshot(self.project), before)

    def test_check_only_validates_before_archive_without_writing(self):
        _, roadmap = self.initialize()
        self.terminal(roadmap)
        before = self.snapshot(self.project)
        self.invoke("create_goal.py", "--check-only", payload=self.payload())
        self.assertEqual(self.snapshot(self.project), before)
        self.invoke("archive_goal.py", "--title", "old-goal")
        self.assertEqual(list(roadmap.iterdir()), [])
        self.invoke("create_goal.py", payload=self.payload())

    def test_invalid_structured_input_leaves_project_untouched(self):
        self.initialize(goal=False)
        baseline = self.snapshot(self.project)
        mutations = [
            lambda p: p.pop("goal"),
            lambda p: p.update(unknown="must not be ignored"),
            lambda p: p.update(goal="  "),
            lambda p: p.update(acceptance=[]),
            lambda p: p.update(milestones=[]),
            lambda p: p["milestones"][0].update(phases=[]),
            lambda p: p["milestones"][0]["phases"][0].update(dependencies=["missing"]),
            lambda p: p["milestones"][0]["phases"][0].update(id="1"),
            lambda p: p["milestones"][0]["phases"][0].update(commit="Phase 1.1: invalid style"),
            lambda p: p["milestones"][0]["review"].pop("verification"),
            lambda p: p.update(progress="fake history"),
        ]
        for mutation in mutations:
            payload = copy.deepcopy(self.payload())
            mutation(payload)
            self.invoke("create_goal.py", payload=payload, success=False)
            self.assertEqual(self.snapshot(self.project), baseline)
        for raw in ('{"goal":"one","goal":"two"}', '{', '[]'):
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/create_goal.py"),
                                     "--project", str(self.project)], input=raw, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(self.snapshot(self.project), baseline)

    def test_phase_style_targets_follow_configuration(self):
        self.invoke("init_project.py", "--mode", "collaborative", "--commit-message-style", "phase")
        payload = self.payload()
        payload["milestones"][0]["phases"][0]["commit"] = "Phase 1.1: implement feature"
        payload["milestones"][0]["review"]["commit"] = "Phase 1.1 Milestone Review: review feature"
        self.invoke("create_goal.py", payload=payload)
        plan = (self.base / "roadmap/milestones.md").read_text()
        self.assertIn("Phase 1.1 Milestone Review: review feature", plan)

    def test_dependencies_follow_an_executable_plan_order(self):
        self.initialize(goal=False)
        baseline = self.snapshot(self.project)
        payload = self.payload()
        first = payload["milestones"][0]
        second = copy.deepcopy(first)
        second["id"] = "2"
        second["phases"][0]["id"] = "2.1"
        payload["milestones"].append(second)
        cases = []
        cyclic = copy.deepcopy(payload)
        cyclic["milestones"][0]["dependencies"] = ["2"]
        cyclic["milestones"][1]["dependencies"] = ["1"]
        cases.append(cyclic)
        forward = copy.deepcopy(payload)
        forward["milestones"][0]["phases"][0]["dependencies"] = ["2.1"]
        cases.append(forward)
        own_parent = copy.deepcopy(payload)
        own_parent["milestones"][0]["phases"][0]["dependencies"] = ["1"]
        cases.append(own_parent)
        for invalid in cases:
            for arguments in ((), ("--check-only",)):
                self.invoke("create_goal.py", *arguments, payload=invalid, success=False)
                self.assertEqual(self.snapshot(self.project), baseline)
        second["dependencies"] = ["1"]
        second["phases"][0]["dependencies"] = ["1.1"]
        self.invoke("create_goal.py", "--check-only", payload=payload)
        self.assertEqual(self.snapshot(self.project), baseline)
        self.invoke("create_goal.py", payload=payload)


if __name__ == "__main__":
    unittest.main()

"""Isolated project-state lifecycle tests; keep failure evidence in private work."""

from datetime import date
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
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

    def invoke(self, command, *args, success=True):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / command), "--project", str(self.project), *args],
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def snapshot(self, path):
        return {str(p.relative_to(path)): p.read_bytes() for p in path.rglob("*") if p.is_file()}

    def initialize(self, mode="collaborative"):
        self.invoke("init_project.py", "--mode", mode)
        folder = self.base / "private" if mode == "privacy" else self.base
        return folder, folder / "roadmap"

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
        self.assertEqual({p.name for p in (config.parent / "roadmap").iterdir()}, set(state.DOCUMENTS))

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

    def test_archive_rebuild_both_modes_includes_hidden_and_nested_files(self):
        for mode, terminal in (("collaborative", "completed"), ("privacy", "cancelled")):
            with self.subTest(mode=mode):
                project = self.project / mode
                project.mkdir()
                roadmap = state.initialize(project, mode)
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
                self.assertEqual({p.name for p in roadmap.iterdir()}, set(state.DOCUMENTS))
                self.assertEqual((roadmap.parent / "config.yaml").read_bytes(), config)
                self.assertEqual(self.snapshot(work), old_work)
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
        self.terminal(roadmap, "cancelled")
        self.invoke("archive_goal.py", "--title", "different-goal")
        self.assertTrue((archive / f"{date.today():%Y%m%d}ab-different-goal/status.md").is_file())

    def test_archive_failure_restores_old_goal_at_both_moving_stages(self):
        _, roadmap = self.initialize()
        self.terminal(roadmap)
        (roadmap / "custom").mkdir()
        (roadmap / "custom/evidence").write_text("preserve")
        original = self.snapshot(roadmap)
        original_move = state.move
        for stage in ("archive", "activate"):
            with self.subTest(stage=stage):
                calls = 0

                def failing_move(source, destination):
                    nonlocal calls
                    relevant = (source.parent == roadmap if stage == "archive" else source.parent.name.startswith("goal-"))
                    if relevant:
                        calls += 1
                        if calls == 3:
                            raise OSError("injected move failure")
                    original_move(source, destination)

                with patch.object(state, "move", side_effect=failing_move):
                    with self.assertRaisesRegex(state.StateError, "original goal restored"):
                        state.archive(self.project, "old-goal")
                self.assertEqual(self.snapshot(roadmap), original)
                self.assertEqual(list((roadmap.parent / "archive").iterdir()), [])

    def test_rollback_failure_reports_paths_and_retains_all_content(self):
        _, roadmap = self.initialize()
        self.terminal(roadmap)
        original = self.snapshot(roadmap)
        original_move = state.move
        activation = 0

        def failing_move(source, destination):
            nonlocal activation
            if source.parent.name.startswith("goal-"):
                activation += 1
                if activation == 2:
                    raise OSError("activation failure")
            if source.parent == roadmap:
                if destination.parent.name.startswith("goal-"):
                    raise OSError("restoration failure")
            original_move(source, destination)

        with patch.object(state, "move", side_effect=failing_move):
            with self.assertRaisesRegex(state.StateError, "recovery also failed.*staging"):
                state.archive(self.project, "old-goal")
        destination = next((roadmap.parent / "archive").iterdir())
        self.assertEqual(self.snapshot(destination), original)

    def test_missing_template_and_state_symlink_do_not_move_old_goal(self):
        fresh_project = self.project / "fresh"
        fresh_project.mkdir()
        with patch.object(state, "PACKAGE", self.project / "missing-package"):
            with self.assertRaises(OSError):
                state.initialize(fresh_project, "privacy")
        self.assertEqual(list(fresh_project.iterdir()), [])
        _, roadmap = self.initialize()
        self.terminal(roadmap)
        before = self.snapshot(self.project)
        with patch.object(state, "PACKAGE", self.project / "missing-package"):
            with self.assertRaises(OSError):
                state.archive(self.project, "old-goal")
        self.assertEqual(self.snapshot(self.project), before)
        external = self.project / "external-archive"
        external.mkdir()
        (roadmap.parent / "archive").symlink_to(external, target_is_directory=True)
        self.invoke("archive_goal.py", "--title", "old-goal", success=False)
        self.assertEqual(list(external.iterdir()), [])


if __name__ == "__main__":
    unittest.main()

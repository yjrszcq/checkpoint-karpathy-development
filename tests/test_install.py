"""Isolated installer integration tests; fixtures remain in ignored private work."""

import os
import json
from pathlib import Path
import pty
import select
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "install.sh"
NAME = "checkpoint-karpathy-development"
PROJECT_DIRS = {
    "claude": ".claude/skills",
    "codex": ".agents/skills",
    "pi": ".pi/skills",
    "ohmypi": ".omp/skills",
    "antigravity": ".agents/skills",
    "cursor": ".cursor/skills",
    "deepseek": ".dsh/skills",
    "gemini": ".gemini/skills",
    "opencode": ".opencode/skills",
}
WORK = ROOT / ".checkpoint-karpathy/private/work/verification/install"


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        WORK.mkdir(parents=True, exist_ok=True)
        cls.run_root = Path(tempfile.mkdtemp(prefix="run-", dir=WORK))
        print(f"Installer test evidence: {cls.run_root}", flush=True)

    def setUp(self):
        self.case = self.run_root / self._testMethodName
        self.case.mkdir()
        self.project = self.case / "project with spaces"
        self.project.mkdir()
        self.env = os.environ.copy()
        # Isolate installer state without changing HOME or actual harness settings.
        self.env.update(
            XDG_STATE_HOME=str(self.case / "state"),
            XDG_CACHE_HOME=str(self.case / "cache"),
        )
        self.base = ["--harness", "codex", "--project", str(self.project)]

    def invoke(self, *args, source=True, success=True):
        command = ["bash", str(SCRIPT), *args]
        if source:
            command += ["--source", str(ROOT)]
        result = subprocess.run(
            command, env=self.env, capture_output=True, text=True,
            timeout=30, start_new_session=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def target(self):
        return self.project / PROJECT_DIRS["codex"] / NAME

    def assert_package(self, target):
        self.assertEqual((target / "SKILL.md").read_bytes(), (ROOT / "SKILL.md").read_bytes())
        for resource in ("references", "scripts", "assets"):
            source_files = sorted(p.relative_to(ROOT / resource) for p in (ROOT / resource).rglob("*") if p.is_file())
            installed_files = sorted(p.relative_to(target / resource) for p in (target / resource).rglob("*") if p.is_file())
            self.assertEqual(source_files, installed_files)
            for file in source_files:
                self.assertEqual((target / resource / file).read_bytes(), (ROOT / resource / file).read_bytes())
        self.assertEqual({p.name for p in target.iterdir()}, {"SKILL.md", "references", "scripts", "assets"})

    def test_all_project_harnesses_and_shared_destination(self):
        result = self.invoke("--harness", ",".join(PROJECT_DIRS), "--project", str(self.project))
        for directory in set(PROJECT_DIRS.values()):
            self.assert_package(self.project / directory / NAME)
        self.assertEqual(result.stdout.count("Installed:"), len(set(PROJECT_DIRS.values())))
        self.assertFalse((self.project / ".checkpoint-karpathy").exists())

    def test_repeat_install_preserves_project_instructions_and_custom_files(self):
        for filename in ("AGENTS.md", "CLAUDE.md", ".gitignore"):
            (self.project / filename).write_text("existing project instructions\n")
        self.invoke(*self.base)
        custom = self.target() / "custom.txt"
        custom.write_text("local customization")
        result = self.invoke(*self.base)
        self.assertIn("Already up to date:", result.stdout)
        self.assertEqual(custom.read_text(), "local customization")
        self.assertFalse(any((self.case / "state").rglob("previous-*")))
        for filename in ("AGENTS.md", "CLAUDE.md", ".gitignore"):
            self.assertEqual((self.project / filename).read_text(), "existing project instructions\n")

    def test_installed_helpers_initialize_create_archive_and_create(self):
        self.invoke(*self.base)
        scripts = self.target() / "scripts"
        payload = {
            "goal": "Installed package creates actual plans", "acceptance": ["Lifecycle succeeds"],
            "included": ["Actual goal"], "non_goals": [], "work_mode": "maintenance",
            "initial_state": "No goal yet", "current_state": "Ready", "next_action": "Execute A.1",
            "context": {"constraints": [], "assumptions": [], "risks": [], "blockers": []},
            "milestones": [{"id": "A", "title": "Delivery", "purpose": "Meet goal", "dependencies": [],
                "phases": [{"id": "A.1", "title": "Implement", "scope": "Lifecycle", "dependencies": [],
                    "success_criteria": "Works", "verification": "Run lifecycle", "commit": "feat(state): implement goal"}],
                "review": {"verification": "Regression checks", "commit": "chore(review): verify goal"}}],
        }
        for script, args in (
            ("init_project.py", ["--mode", "privacy", "--language", "zh"]),
            ("create_goal.py", []),
            ("archive_goal.py", ["--title", "installed-goal"]),
            ("create_goal.py", []),
        ):
            result = subprocess.run(
                [sys.executable, "-B", str(scripts / script), "--project", str(self.project), *args],
                env=self.env, capture_output=True, text=True, timeout=15,
                input=json.dumps(payload) if script == "create_goal.py" else "",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            roadmap = self.project / ".checkpoint-karpathy/private/roadmap"
            if script == "init_project.py":
                self.assertEqual(list(roadmap.iterdir()), [])
            if script == "create_goal.py":
                self.assertIn(payload["goal"], (roadmap / "README.md").read_text())
                (roadmap / "status.md").write_text("## Completion\ncancelled\n")
            if script == "archive_goal.py":
                self.assertEqual(list(roadmap.iterdir()), [])
        archive = next((roadmap.parent / "archive").iterdir())
        self.assertIn("cancelled", (archive / "status.md").read_text())
        self.assertIn("Establish initial plan", (roadmap / "changelog.md").read_text())
        self.assert_package(self.target())

    def test_upgrade_backs_up_complete_previous_package_outside_discovery(self):
        self.invoke(*self.base)
        old_skill = "old version\n"
        (self.target() / "SKILL.md").write_text(old_skill)
        (self.target() / "custom.txt").write_text("keep me")
        result = self.invoke(*self.base)
        backups = list((self.case / "state").rglob("previous-codex"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "SKILL.md").read_text(), old_skill)
        self.assertEqual((backups[0] / "custom.txt").read_text(), "keep me")
        self.assertIn(str(backups[0]), result.stdout)
        self.assertEqual(list(self.project.rglob("SKILL.md")), [self.target() / "SKILL.md"])
        self.assert_package(self.target())

    def test_aliases_repeated_flags_and_custom_directory(self):
        aliases = "claudecode,claude-code,codex,pi,omp,oh-my-pi,antigrivaty,cursor,deepseekharness,deepseek-harness,dsh,geminicli,gemini-cli,opencode"
        result = self.invoke("--harness", aliases, "--harness", "codex", "--project", str(self.project), "--dry-run")
        self.assertEqual(len(result.stdout.splitlines()), len(PROJECT_DIRS))
        self.assertEqual(list(self.project.iterdir()), [])
        custom = self.case / "custom skills"
        self.invoke("--harness", "custom", "--skills-dir", str(custom))
        self.assert_package(custom / NAME)

    def test_user_paths_dry_run_only(self):
        # Never perform a real user-scope installation in a developer's HOME.
        result = self.invoke("--harness", ",".join(PROJECT_DIRS), "--scope", "user", "--dry-run", source=False)
        home = Path.home()
        expected = {
            "claude": Path(self.env.get("CLAUDE_CONFIG_DIR", home / ".claude")) / "skills",
            "codex": home / ".agents/skills",
            "pi": Path(self.env.get("PI_CODING_AGENT_DIR", home / ".pi/agent")) / "skills",
            "ohmypi": home / ".omp/agent/skills",
            "antigravity": home / ".gemini/config/skills",
            "cursor": home / ".cursor/skills",
            "deepseek": Path(self.env.get("DSH_HOME", home / ".dsh")) / "skills",
            "gemini": home / ".gemini/skills",
            "opencode": Path(self.env.get("XDG_CONFIG_HOME", home / ".config")) / "opencode/skills",
        }
        for harness, directory in expected.items():
            self.assertIn(f"{harness} (user): {directory / NAME}\n", result.stdout)
        self.assertFalse((self.case / "state").exists())
        self.assertFalse((self.case / "cache").exists())

    def test_invalid_arguments_and_incomplete_source_preserve_install(self):
        self.invoke(*self.base)
        before = (self.target() / "SKILL.md").read_bytes()
        broken = self.case / "incomplete source"
        broken.mkdir()
        shutil.copyfile(ROOT / "SKILL.md", broken / "SKILL.md")
        for args in (
            ["--harness", "missing"], ["--harness"],
            ["--harness", "codex", "--scope", "missing"],
            ["--harness", "codex", "--project", str(self.project), "--scope", "user"],
            ["--harness", "custom"],
            ["--harness", "custom,codex"],
            ["--harness", "codex,cursor", "--skills-dir", str(self.case / "skills")],
            [*self.base, "--source", str(broken)],
        ):
            with self.subTest(args=args):
                self.invoke(*args, source=False, success=False)
                self.assertEqual((self.target() / "SKILL.md").read_bytes(), before)

    def test_user_directory_overrides_without_installing(self):
        overrides = {
            "claude": ("CLAUDE_CONFIG_DIR", "claude config"),
            "pi": ("PI_CODING_AGENT_DIR", "pi agent"),
            "deepseek": ("DSH_HOME", "deepseek home"),
            "opencode": ("XDG_CONFIG_HOME", "xdg config"),
        }
        for harness, (variable, directory) in overrides.items():
            self.env[variable] = str(self.case / directory)
        result = self.invoke("--harness", ",".join(overrides), "--dry-run")
        for harness, (_, directory) in overrides.items():
            parent = self.case / directory
            if harness == "opencode":
                parent /= "opencode"
            self.assertIn(f"{harness} (user): {parent / 'skills' / NAME}\n", result.stdout)
            self.assertFalse(parent.exists())

    def fake_tool(self, name, code):
        directory = self.case / "bin"
        directory.mkdir(exist_ok=True)
        executable = directory / name
        executable.write_text(f"#!{sys.executable}\n" + code)
        executable.chmod(0o755)
        self.env["PATH"] = str(directory) + os.pathsep + os.environ["PATH"]

    def test_downloaded_package_ref_and_full_references(self):
        archive = self.case / "release.tar.gz"
        with tarfile.open(archive, "w:gz") as bundle:
            bundle.add(ROOT / "SKILL.md", arcname="release/SKILL.md")
            for resource in ("references", "scripts", "assets"):
                bundle.add(ROOT / resource, arcname="release/" + resource)
            bundle.add(ROOT / "AGENTS.md", arcname="release/AGENTS.md")
        self.env["TEST_ARCHIVE"] = str(archive)
        self.env["TEST_REQUEST"] = str(self.case / "request.txt")
        self.fake_tool("curl", "import os, shutil, sys\nfrom pathlib import Path\na=sys.argv[1:]\nPath(os.environ['TEST_REQUEST']).write_text(' '.join(a))\nshutil.copyfile(os.environ['TEST_ARCHIVE'], a[a.index('-o')+1])\n")
        result = self.invoke(*self.base, "--ref", "v1.2.3", source=False)
        self.assertIn("/tar.gz/v1.2.3", (self.case / "request.txt").read_text())
        self.assertIn("Reusable source cache:", result.stdout)
        self.assert_package(self.target())
        self.assertFalse((self.target() / "AGENTS.md").exists())

    def test_download_failure_preserves_previous_install(self):
        self.invoke(*self.base)
        before = (self.target() / "SKILL.md").read_bytes()
        self.fake_tool("curl", "raise SystemExit(22)\n")
        self.invoke(*self.base, source=False, success=False)
        self.assertEqual((self.target() / "SKILL.md").read_bytes(), before)

    def test_activation_failure_restores_previous_and_preserves_partial_output(self):
        self.invoke(*self.base)
        (self.target() / "SKILL.md").write_text("previous version")
        self.fake_tool("mv", "import os, sys\nfrom pathlib import Path\na=sys.argv[1:]\nif Path(a[-2]).name.startswith('staged-'):\n Path(a[-1]).mkdir()\n (Path(a[-1])/'partial.txt').write_text('partial output')\n raise SystemExit(1)\nos.execv('/bin/mv', ['/bin/mv', *a])\n")
        result = self.invoke(*self.base, success=False)
        self.assertEqual((self.target() / "SKILL.md").read_text(), "previous version")
        self.assertIn("Restored previous installation:", result.stderr)
        partial = list((self.case / "state").rglob("interrupted-install/partial.txt"))
        self.assertEqual(len(partial), 1)
        self.assertEqual(partial[0].read_text(), "partial output")

    def test_fresh_activation_failure_keeps_partial_bundle_outside_discovery(self):
        self.fake_tool("mv", "import sys\nfrom pathlib import Path\na=sys.argv[1:]\nif Path(a[-2]).name.startswith('staged-'):\n Path(a[-1]).mkdir()\n (Path(a[-1])/'partial.txt').write_text('partial output')\n raise SystemExit(1)\nimport os\nos.execv('/bin/mv', ['/bin/mv', *a])\n")
        self.invoke(*self.base, success=False)
        self.assertFalse(self.target().exists())
        partial = list((self.case / "state").rglob("interrupted-install/partial.txt"))
        self.assertEqual(len(partial), 1)

    def test_symlink_replacement_preserves_original_link_target(self):
        previous = self.case / "old bundle"
        previous.mkdir()
        (previous / "SKILL.md").write_text("external version")
        self.target().parent.mkdir(parents=True)
        self.target().symlink_to(previous, target_is_directory=True)
        self.invoke(*self.base)
        self.assertFalse(self.target().is_symlink())
        self.assertEqual((previous / "SKILL.md").read_text(), "external version")
        backup = list((self.case / "state").rglob("previous-codex"))
        self.assertEqual(len(backup), 1)
        self.assertTrue(backup[0].is_symlink())
        self.assert_package(self.target())

    def test_no_terminal_requires_harness(self):
        result = self.invoke("--project", str(self.project), success=False)
        self.assertIn("Specify --harness", result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])

    def run_interactive(self, answers, success=True):
        command = f"cat {shlex.quote(str(SCRIPT))} | bash -s -- --source {shlex.quote(str(ROOT))}"
        pid, master = pty.fork()
        if pid == 0:
            os.chdir(self.project)
            os.execve("/bin/bash", ["bash", "-c", command], self.env)
        transcript = b""
        answered = 0
        reaped = False
        exit_code = None
        deadline = time.monotonic() + 30
        try:
            while time.monotonic() < deadline:
                ready, _, _ = select.select([master], [], [], 0.1)
                if ready:
                    try:
                        data = os.read(master, 65536)
                    except OSError:
                        break
                    if not data:
                        break
                    transcript += data
                    while answered < len(answers) and answers[answered][0] in transcript:
                        os.write(master, answers[answered][1] + b"\n")
                        answered += 1
                done, status = os.waitpid(pid, os.WNOHANG)
                if done:
                    reaped = True
                    exit_code = os.waitstatus_to_exitcode(status)
                    break
            else:
                self.fail("Interactive installer timed out: " + transcript.decode())
            if not reaped:
                _, status = os.waitpid(pid, 0)
                reaped = True
                exit_code = os.waitstatus_to_exitcode(status)
        finally:
            if not reaped:
                os.kill(pid, 15)
                os.waitpid(pid, 0)
            os.close(master)
        self.assertEqual(answered, len(answers), transcript.decode())
        if success:
            self.assertEqual(exit_code, 0, transcript.decode())
        else:
            self.assertNotEqual(exit_code, 0, transcript.decode())
        return transcript.decode()

    def test_interactive_selection_when_script_is_piped(self):
        self.run_interactive([(b"> ", b"2,6"), (b"Install scope:", b"2")])
        self.assert_package(self.target())
        self.assert_package(self.project / PROJECT_DIRS["cursor"] / NAME)

    def test_interactive_custom_installation_by_number_and_name(self):
        for choice in (b"10", b"custom"):
            with self.subTest(choice=choice):
                parent = self.case / ("custom skills " + choice.decode())
                # Relative paths and spaces must survive terminal input unchanged.
                relative = os.path.relpath(parent, self.project)
                transcript = self.run_interactive([
                    (b"> ", choice),
                    (b"Skills directory", relative.encode()),
                ])
                self.assertIn("custom (enter installation path)", transcript)
                self.assertNotIn("Install scope:", transcript)
                self.assert_package(parent / NAME)

    def test_interactive_custom_rejects_empty_path_and_mixed_selection(self):
        transcript = self.run_interactive([
            (b"> ", b"custom"), (b"Skills directory", b"   "),
        ], success=False)
        self.assertIn("No installation path entered.", transcript)
        transcript = self.run_interactive([(b"> ", b"custom,2")], success=False)
        self.assertIn("Select custom on its own.", transcript)
        self.assertFalse((self.case / "state").exists())
        self.assertEqual(list(self.project.iterdir()), [])

    def test_custom_home_path_dry_run(self):
        result = self.invoke(
            "--harness", "custom", "--skills-dir", "~/custom skills", "--dry-run",
        )
        self.assertIn(str(Path.home() / "custom skills" / NAME), result.stdout)
        self.assertFalse((self.case / "state").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)

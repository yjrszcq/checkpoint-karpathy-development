# Installation guide for agents

If a user sends this repository URL and asks you to install the skill, follow this document.

Repository: <https://github.com/yjrszcq/checkpoint-karpathy-development>

## Choose the destination

Use the harness and installation scope specified by the user. Otherwise, use the current harness and user scope. If the current harness cannot be identified, ask which harness to use.

Choose the actual installation location from the user's request and the active harness configuration. The paths below are defaults; inspect local discovery settings, active profiles, and existing installations as needed. Use the directory the running harness actually discovers, passing `--skills-dir` for a custom location. If the user gives the final `checkpoint-karpathy-development/` directory, pass its parent as `--skills-dir`.

The installer supports Bash 3.2+ on Linux, macOS, and WSL. Remote installation needs `curl` and `tar`; local installation also works offline with `--source`. On other environments, use the manual package-copy procedure below and the harness's supported paths.

Standard skills parent directories are listed below. Each receives a `checkpoint-karpathy-development/` child directory. Links point to the harness's documentation or discovery implementation.

| `--harness` | User scope | Project scope |
|---|---|---|
| [claude](https://code.claude.com/docs/en/skills) | `~/.claude/skills/` | `.claude/skills/` |
| [codex](https://developers.openai.com/codex/skills/) | `~/.agents/skills/` | `.agents/skills/` |
| [pi](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) | `~/.pi/agent/skills/` | `.pi/skills/` |
| [ohmypi](https://github.com/can1357/oh-my-pi/blob/main/packages/coding-agent/src/discovery/builtin.ts) | `~/.omp/agent/skills/` | `.omp/skills/` |
| [antigravity](https://antigravity.google/docs/skills) | `~/.gemini/config/skills/` | `.agents/skills/` |
| [cursor](https://cursor.com/docs/context/skills) | `~/.cursor/skills/` | `.cursor/skills/` |
| [deepseek](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md) | `~/.dsh/skills/` | `.dsh/skills/` |
| [gemini](https://geminicli.com/docs/cli/skills/) | `~/.gemini/skills/` | `.gemini/skills/` |
| [opencode](https://opencode.ai/docs/skills/) | `~/.config/opencode/skills/` | `.opencode/skills/` |

`claudecode` / `claude-code`, `omp` / `oh-my-pi`, `deepseekharness` / `deepseek-harness` / `dsh`, and `geminicli` / `gemini-cli` are accepted aliases. Multiple harnesses can be comma-separated or supplied with repeated `--harness` flags. Identical destination paths are installed once.

The installer honors `CLAUDE_CONFIG_DIR`, `PI_CODING_AGENT_DIR`, `DSH_HOME`, and `XDG_CONFIG_HOME` for the corresponding user paths. For profiles, custom homes, or other configuration overrides, determine the actual discovery directory and pass `--skills-dir /absolute/path/to/skills`. For example, an Oh My Pi named profile normally uses `~/.omp/profiles/<name>/agent/skills/`; pass that active profile directory explicitly. With this option select just one harness. Other compatible harnesses can use `--harness custom --skills-dir PATH`; confirm their discovery rules first.

Several harnesses also read shared `.agents/skills/` or other tools' directories. Check for an existing installation before adding another copy; a shared copy may already satisfy the user's request. Resolve differing existing copies with the user before proceeding.

## Install

If you have a local checkout, inspect `install.sh`, `SKILL.md`, and the linked references, then run from the checkout:

```bash
bash install.sh --harness codex --scope user --source .
```

Use the chosen harness in place of `codex`. For project scope, supply the actual project root:

```bash
bash install.sh --harness claude --project /absolute/path/to/project --source .
```

Use `--dry-run` first when you need to check the resolved destination; it writes nothing and does not download. `--skills-dir` names the parent skills directory.

For a custom location, select the known harness with `--skills-dir`, or use `custom` for another compatible harness:

```bash
bash install.sh --harness custom --skills-dir "/actual/path/to/skills" --source .
```

This installs into `/actual/path/to/skills/checkpoint-karpathy-development/`. Relative paths resolve from the current working directory; a leading `~/` resolves under the user's home directory.

Without a checkout, download and inspect the installer before executing it, or use the user's requested remote command:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash -s -- --harness codex --scope user
```

For interactive human installation, omit the arguments after `bash`. Select `custom` on its own to enter a skills parent directory manually; no scope selection is needed for this explicit path. The menu reads interactive input from `/dev/tty`. Agents should pass explicit arguments. Without a terminal, omitting `--harness` fails with guidance.

`--ref` chooses the downloaded package's branch, tag, or commit; the default is `main`. To pin the installer as well, use that same ref in the raw installer URL. Remote source files are cached under `${XDG_CACHE_HOME:-~/.cache}/checkpoint-karpathy-installer/`; the installer prints a reusable `--source` path. A failed download or incomplete package leaves existing installations untouched.

The installed package contains only:

```text
checkpoint-karpathy-development/
  SKILL.md
  references/
    checkpoint-details.md
    project-state.md
    goal-input.md
    roadmap-templates.md
  scripts/
    init_project.py
    create_goal.py
    archive_goal.py
    project_state.py
    goal_documents.py
    requirements.txt
  assets/
    config/
      en.yaml
      zh.yaml
    roadmap/
      README.md
      status.md
      context.md
      milestones.md
      milestone.md
      phase.md
      changelog.md
      progress.md
```

Install the root `SKILL.md` and complete `references/`, `scripts/`, and `assets/` directories into the selected skill directory, preserving their relative structure. The repository root is the canonical package source. Keep installation confined to that destination.

## Updates and recovery

Run the same command to update. An identical package is left in place. Before replacing an existing bundle, the installer stages and checks the new package, then moves the complete old bundle to a unique backup outside skill discovery:

```text
${XDG_STATE_HOME:-~/.local/state}/checkpoint-karpathy-installer/backups/
  <timestamp>.<unique-id>/
    previous-<harness>/
```

The printed backup path includes custom files from the previous installation. If activation fails, the installer attempts to restore that bundle and retains partial output for inspection. Updates are independent per destination; successful earlier installations remain if a later destination fails.

For manual restoration, first move the current installed bundle to a separate location outside all scanned skills directories, then move the printed previous bundle back to its original installation path. Preserve both versions until the restored skill is verified. Do not put backup skill directories under any `skills/` directory.

If shell installation is unavailable, copy root `SKILL.md` and the complete `references/`, `scripts/`, and `assets/` directories into the destination shown above, preserving their relative structure. Stage and verify the new package first, back up any existing bundle outside discovery, and restore it if replacement fails. Respect the user's environment and deletion rules.

The project-state helpers require Python 3.9+ and PyYAML. Verify the Python environment before using them; if PyYAML is missing, install it in a suitable environment with `python3 -m pip install -r /path/to/checkpoint-karpathy-development/scripts/requirements.txt`.

## Verify and report

Check that installed `SKILL.md` has `name: checkpoint-karpathy-development`, that every relative reference resolves, and that installed content matches the selected source. Confirm the actual installation path is one the selected harness discovers. File copying alone does not prove runtime discovery.

Restart the harness or use its supported reload action, then inspect its skills list when available. Report which of these you verified and whether a restart or user-side discovery check remains. Typical explicit invocations are `$checkpoint-karpathy-development` in Codex, `/checkpoint-karpathy-development` in Claude Code, and `/skill:checkpoint-karpathy-development` in Pi and Oh My Pi. A natural-language request to use the skill also works where the harness supports model-selected skills.

Tell the user the harness, scope, destination, verification result, and backup path if one was created. Do not start a development goal merely to test installation.

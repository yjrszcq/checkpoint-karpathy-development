# Checkpoint Karpathy Agent Workflow

English | [简体中文](README_CN.md)

A roadmap-driven development skill with Karpathy-inspired engineering guardrails. The agent plans the full goal, verifies and commits each subphase, and records progress so work can resume across sessions and context loss.

Works with Codex, Claude Code, Pi, Oh My Pi, Antigravity, Cursor, DeepSeek Harness, and other compatible agents.

## Quick installation

The project-state helpers require **Python 3.9+** and **PyYAML >= 6.0** for project initialization, roadmap generation, and archiving. See [dependency setup](docs/guide.md#project-state-commands).

Run the installer and select your harness and installation scope:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash
```

Or specify them directly:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash -s -- --harness codex --scope user
```

For custom paths, project installations, and other harnesses, see the [installation options](docs/guide.md#installation).

### Let your agent install it

Send this request to your agent:

```text
Install this skill for my current harness by following INSTALL.md in the repository:
https://github.com/yjrszcq/checkpoint-karpathy-development
```

You can specify a harness, project scope, or custom installation path in the request. See the [agent installation guide](INSTALL.md) for details.

## Usage

Restart or reload your harness after installation, then ask:

```text
Use checkpoint-karpathy-development to help me complete: <goal>
```

The defaults are collaborative visibility and Conventional Commits. Settings persist in `config.yaml`; privacy mode keeps planning documents out of Git. Goal documents live in a fixed `roadmap/` directory, with separate overview, status, context, milestones, plan changes, and execution history.

## Documentation

- [Usage guide](docs/guide.md): configuration, project-state commands, roadmap lifecycle, and temporary files.
- [Agent installation guide](INSTALL.md): installation paths, updates, backups, and verification.
- [Skill instructions](SKILL.md): the agent's workflow and supporting references.

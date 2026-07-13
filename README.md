# Checkpoint Karpathy Agent Workflow

English | [简体中文](README_CN.md)

A Codex + Claude Code workflow for roadmap-driven, checkpointed software development with Karpathy-inspired engineering guardrails.

It is designed for greenfield development, mid-project continuation, feature work, bug fixing, refactoring, late-stage maintenance, and handoffs where work must stay recoverable across quota limits, session resets, and context loss.

## Core idea

Before substantial work, the agent creates or updates a roadmap that plans completely from the current state to the full achievement of all stated goals.

Once active, the skill stays active across conversations until the roadmap is complete. Each new development conversation automatically resumes from the next unfinished subphase — the user does not need to re-invoke it.

When the roadmap is complete, the skill deactivates. If the user later asks to use it again for a new goal, the completed roadmap and progress are archived to `.checkpoint-karpathy/archive/YYYY-MM-DD-<summary>/`.

Each normal subphase must end with:

- a completed roadmap item,
- project-appropriate verification,
- an updated progress log,
- a Git commit,
- and a clear next step.

Commit messages use one of two styles:

Phase-style (default):
```text
Phase X.Y: <description>
```

Professional-style (Conventional Commits):
```text
type(scope): <English summary>
```

Description defaults to English. Use another language only when the user asks.

When a major milestone is complete, the agent must perform a standalone milestone review checkpoint before moving on. This checkpoint does not consume the next planned Phase/Subphase number; it confirms scope, simplifies milestone work, runs the broadest relevant verification, reviews for regressions or integration gaps, debugs and fixes in-scope issues, reruns verification, records progress, and commits the closeout.

The engineering guardrails are:

- think before coding,
- keep the solution simple,
- make surgical changes in existing codebases,
- verify against a concrete goal.

## Repository state

The workflow uses a namespaced directory:

**Collaborative mode:**
```text
.checkpoint-karpathy/
  roadmap.md
  progress.md
  private/
  archive/
```

**Privacy mode:**
```text
.checkpoint-karpathy/
  private/
    roadmap.md
    progress.md
    archive/
```

Default collaborative mode:

- commit `.checkpoint-karpathy/roadmap.md`,
- commit `.checkpoint-karpathy/progress.md`,
- ignore `.checkpoint-karpathy/private/`.

Privacy mode:

- place `roadmap.md` and `progress.md` inside `.checkpoint-karpathy/private/`,
- keep `.checkpoint-karpathy/private/` ignored by Git,
- do not commit roadmap or progress.

Use privacy mode for public repositories or when development planning should not be exposed.

## Install for Codex

Copy the skill into Codex's project or user skill directory:

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp .codex/skills/checkpoint-karpathy-development/SKILL.md ~/.codex/skills/checkpoint-karpathy-development/SKILL.md
```

For project-level Codex instructions, copy:

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

Use it:

```text
$checkpoint-karpathy-development

Read AGENTS.md. Create or update .checkpoint-karpathy/roadmap.md for this task, complete one roadmap subphase, update .checkpoint-karpathy/progress.md, run project-appropriate verification, and git commit.
```

## Install for Claude Code

For project-level Claude Code instructions, copy:

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
```

Copy the Claude Code skill:

```bash
mkdir -p /path/to/your/project/.claude/skills/checkpoint-karpathy-development
cp .claude/skills/checkpoint-karpathy-development/SKILL.md /path/to/your/project/.claude/skills/checkpoint-karpathy-development/SKILL.md
```

Optional slash command:

```bash
mkdir -p /path/to/your/project/.claude/commands
cp .claude/commands/checkpoint-karpathy.md /path/to/your/project/.claude/commands/checkpoint-karpathy.md
```

Use it:

```text
/checkpoint-karpathy Continue this project using checkpoint-karpathy development. Select the work mode, update the roadmap, complete one subphase, update progress, verify, and commit.
```

## Gitignore

Add one line to `.gitignore`:

```gitignore
.checkpoint-karpathy/private/
```

In privacy mode, `roadmap.md` and `progress.md` live inside `private/` and are covered automatically. In collaborative mode, this keeps sensitive notes out of version control.

Do not ignore `.checkpoint-karpathy/` wholesale unless you intentionally want to hide all workflow state.

Do not ignore `.checkpoint-karpathy/` wholesale unless you intentionally want to hide all workflow state.

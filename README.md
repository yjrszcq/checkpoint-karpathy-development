# Checkpoint Karpathy Agent Workflow

English | [简体中文](README_CN.md)

A Codex + Claude Code workflow for roadmap-driven, checkpointed software development with Karpathy-inspired engineering guardrails.

It is designed for greenfield development, mid-project continuation, feature work, bug fixing, refactoring, late-stage maintenance, and handoffs where work must stay recoverable across quota limits, session resets, and context loss.

## Core idea

Before substantial work, the agent creates or updates a roadmap. Then it works one commit-sized subphase at a time.

Each normal subphase must end with:

- a completed roadmap item,
- project-appropriate verification,
- an updated progress log,
- a Git commit using an English Conventional Commits-style message unless the user requests another language,
- and a clear next step.

When a major milestone is complete, the agent must perform a standalone milestone review checkpoint before moving on. This checkpoint does not consume the next planned Phase/Subphase number; it confirms scope, simplifies milestone work, runs the broadest relevant verification, reviews for regressions or integration gaps, debugs and fixes in-scope issues, reruns verification, records progress, and commits the closeout.

The engineering guardrails are:

- think before coding,
- keep the solution simple,
- make surgical changes in existing codebases,
- verify against a concrete goal.

Commit messages default to standard engineering style:

```text
type(scope): English summary
```

For example, `fix(web): update stale button state` or `docs(skill): require conventional commit messages`. Use another language only when the user asks for it.

## Repository state

The workflow uses a namespaced directory:

```text
.checkpoint-karpathy/
  roadmap.md
  progress.md
  private/
```

Default collaborative mode:

- commit `.checkpoint-karpathy/roadmap.md`,
- commit `.checkpoint-karpathy/progress.md`,
- ignore `.checkpoint-karpathy/private/`.

Privacy mode:

- ignore `.checkpoint-karpathy/roadmap.md`,
- ignore `.checkpoint-karpathy/progress.md`,
- ignore `.checkpoint-karpathy/private/`.

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

Default collaborative mode:

```gitignore
.checkpoint-karpathy/private/
```

Privacy mode:

```gitignore
.checkpoint-karpathy/roadmap.md
.checkpoint-karpathy/progress.md
.checkpoint-karpathy/private/
```

Do not ignore `.checkpoint-karpathy/` wholesale unless you intentionally want to hide all workflow state.

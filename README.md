# Checkpoint Karpathy Agent Workflow

English | [简体中文](README_CN.md)

A reusable agent workflow for **Codex** and **Claude Code**.

It combines:

1. **Checkpoint-driven development** — split work into small recoverable phases, update `docs/progress.md`, keep scratch output in `.agent-artifacts/`, run verification, and commit every completed phase.
2. **Karpathy-inspired engineering guardrails** — think before coding, keep solutions simple, avoid speculative abstractions, make surgical changes in existing codebases, and verify against explicit goals.

Recommended GitHub repository name:

```text
codex-claude-checkpoint-karpathy-workflow
```

Shorter alternatives:

```text
checkpoint-karpathy-agent-workflow
checkpoint-karpathy-dev-skill
```

## What is included

```text
checkpoint-karpathy-agent-workflow/
  README.md
  SKILL.md                                      # Shared Skill source
  AGENTS.md                                    # Codex project instructions
  CLAUDE.md                                    # Claude Code project memory/instructions
  .gitignore                                   # Ignores .agent-artifacts/
  codex/
    skills/
      checkpoint-karpathy-development/
        SKILL.md                               # Codex install layout
  .claude/
    skills/
      checkpoint-karpathy-development/
        SKILL.md                               # Claude Code Skill layout
    commands/
      checkpoint-karpathy.md                   # Legacy/custom slash command wrapper
```

## When to use it

Use this workflow for:

- greenfield development,
- mid-project continuation,
- feature development,
- bug fixing,
- refactoring,
- late-stage maintenance,
- release preparation,
- documentation/configuration changes that affect development,
- any multi-step coding task where losing uncommitted progress would be expensive.

Do not use it for tiny one-line edits unless you explicitly want every change checkpointed.

## Core behavior

Every completed phase must end with:

- a coherent repository state,
- updated `docs/progress.md`,
- intermediate/scratch artifacts kept under `.agent-artifacts/`,
- `.agent-artifacts/` ignored by Git,
- project-appropriate verification,
- and a Git commit.

A phase is not complete until it is committed.

## Work modes

The agent should classify each task before starting:

| Mode | Use case |
| --- | --- |
| Greenfield Development | Starting a new project from zero |
| Mid-Project Continuation | Continuing an existing codebase or unfinished work |
| Feature Development | Adding a new capability |
| Bug Fixing | Reproducing, diagnosing, and fixing a bug |
| Refactoring | Improving structure while preserving behavior |
| Late-Stage Maintenance | Conservative changes near release or production |

## Codex installation

### Global Skill installation

Copy the Skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp SKILL.md ~/.codex/skills/checkpoint-karpathy-development/SKILL.md
```

Or from this repository layout:

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp codex/skills/checkpoint-karpathy-development/SKILL.md ~/.codex/skills/checkpoint-karpathy-development/SKILL.md
```

### Project instructions

Copy `AGENTS.md` to the target project root:

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

Then start Codex from that project and invoke:

```text
$checkpoint-karpathy-development

Follow the project AGENTS.md. Work in checkpointed phases: update docs/progress.md, keep scratch files in .agent-artifacts/, run project-appropriate verification, and commit every completed phase.
```

## Claude Code installation

Claude Code supports project instructions through `CLAUDE.md` and supports current custom workflow packaging through `.claude/skills/<name>/SKILL.md`. This repository includes both.

### Project-level setup

Copy these files/directories into the target project root:

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
mkdir -p /path/to/your/project/.claude/skills/checkpoint-karpathy-development
cp .claude/skills/checkpoint-karpathy-development/SKILL.md /path/to/your/project/.claude/skills/checkpoint-karpathy-development/SKILL.md
mkdir -p /path/to/your/project/.claude/commands
cp .claude/commands/checkpoint-karpathy.md /path/to/your/project/.claude/commands/checkpoint-karpathy.md
```

Also ensure `.agent-artifacts/` is ignored in the target project:

```bash
grep -qxF '.agent-artifacts/' /path/to/your/project/.gitignore 2>/dev/null || echo '.agent-artifacts/' >> /path/to/your/project/.gitignore
```

### Usage in Claude Code

Use the skill directly if available:

```text
/checkpoint-karpathy-development <your task>
```

Or use the wrapper command included in this repository:

```text
/checkpoint-karpathy <your task>
```

You can also ask in plain language:

```text
Use checkpoint-karpathy development for this task. Follow CLAUDE.md. Work in small phases, update docs/progress.md, keep scratch files in .agent-artifacts/, run project-appropriate verification, and commit each completed phase.
```

## Claude Code global/personal setup

For personal use across projects, you may copy the skill to your Claude user directory:

```bash
mkdir -p ~/.claude/skills/checkpoint-karpathy-development
cp SKILL.md ~/.claude/skills/checkpoint-karpathy-development/SKILL.md
```

Legacy/custom command support:

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/checkpoint-karpathy.md ~/.claude/commands/checkpoint-karpathy.md
```

For project-specific behavior, still keep `CLAUDE.md` in the repository root.

## Intermediate artifacts

Use `.agent-artifacts/` for scratch files, temporary analysis outputs, generated notes, draft plans, logs, and other intermediate files that should not be committed.

Keep persistent handoff information in:

```text
docs/progress.md
```

If an intermediate artifact becomes a real deliverable, move it out of `.agent-artifacts/`, record the decision in `docs/progress.md`, and commit it.

## Git safety

The workflow forbids destructive Git commands unless the user explicitly asks.

Do not run without explicit permission:

```bash
git reset --hard
git clean
git rebase
git commit --amend
git push --force
git checkout -- .
git restore .
git restore --staged .
```

Do not commit unrelated user changes.

Do not commit secrets.

Respect `.gitignore`.

## Suggested first prompt

For Codex:

```text
$checkpoint-karpathy-development

Continue this project using checkpoint-karpathy development. First inspect the repo and select the work mode. Then complete one small phase, update docs/progress.md, keep scratch files in .agent-artifacts/, run project-appropriate verification, and git commit.
```

For Claude Code:

```text
/checkpoint-karpathy Continue this project using checkpoint-karpathy development. First inspect the repo and select the work mode. Then complete one small phase, update docs/progress.md, keep scratch files in .agent-artifacts/, run project-appropriate verification, and git commit.
```

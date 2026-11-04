# Claude Code Instructions: Checkpoint Karpathy Agent Workflow

Use checkpoint-karpathy development for multi-step software work in this project.

## Core behavior

When the user gives a concrete development goal, first read or create `config.md` using Project configuration below. Resolve roadmap and progress paths relative to the configured state directory.

1. Select the work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
2. Create or update `.checkpoint-karpathy/roadmap.md`. The initial roadmap must plan completely from the current state to the full achievement of all stated goals.
3. Split the goal into major milestones and commit-sized subphases.
4. Work on one subphase at a time.
5. Run the smallest project-appropriate verification for normal subphases.
6. Update `.checkpoint-karpathy/progress.md` after each completed subphase.
7. Commit each completed subphase.
8. When a major milestone is complete, perform a standalone milestone review checkpoint before moving on. Do not increment the planned Phase/Subphase number for this closeout; confirm scope, simplify milestone work, run the broadest relevant verification, review for regressions or integration gaps, debug and fix in-scope issues, rerun verification, record progress, and commit the closeout.
9. Keep following the roadmap unless reality changes; if it changes, update the roadmap and record why.

## Skill lifecycle

- **First-time planning:** The roadmap must cover every milestone and subphase needed to achieve all goals. Create `config.md` before roadmap and progress files, recording user-specified settings or the defaults (collaborative mode, Conventional Commits). Briefly state the recorded settings and proceed without asking the user to choose.
- **During execution:** Every development-related conversation must use this skill until the roadmap is complete. A conversation may naturally end (session limit, quota) between subphases — the skill remains active, and the next development conversation should automatically resume from the next unfinished subphase.
- **After completion:** When every subphase and milestone review is done, the skill is no longer active. Do not invoke it again unless the user explicitly asks for checkpoint-karpathy development on a new goal.
- **Re-invocation:** When the user asks to use this skill for a new goal, or when a new conversation continues an unfinished roadmap:
  - Read `config.md` first and apply any settings changes requested by the user.
  - If no roadmap exists, plan from scratch using the recorded settings.
  - If the roadmap is already complete, archive `roadmap.md` and `progress.md` to `.checkpoint-karpathy/archive/YYYYMMDDa-<summary>/` (or `.checkpoint-karpathy/private/archive/YYYYMMDDa-<summary>/` in privacy mode; the letter auto-increments to avoid collisions), then create fresh roadmap and progress files for the new goal. Keep `config.md` in the active directory.
  - If the roadmap is not yet complete, resume from the next unfinished subphase.
  - **Mode persistence:** Use the mode and commit message style recorded in `config.md` across conversations and goals.

## Project configuration

Before each use, look for `.checkpoint-karpathy/config.md` and `.checkpoint-karpathy/private/config.md`. Read the active configuration; if both exist, ask which one to keep before proceeding. If none exists, create one before roadmap and progress files, recording each user-specified setting or its default:

```md
# Checkpoint Karpathy Configuration

- Mode: collaborative
- Commit message style: conventional
```

`Mode` accepts `collaborative` or `privacy`; `Commit message style` accepts `conventional` (Conventional Commits) or `phase` (Phase-style).

Keep `config.md`, `roadmap.md`, and `progress.md` together in `.checkpoint-karpathy/` for collaborative mode or `.checkpoint-karpathy/private/` for privacy mode. Preserve any existing roadmap and progress files when creating the configuration and align their location with the selected mode. On a user-requested settings change, update only the requested values and uncompleted roadmap commit targets. When the mode changes, move the active three files together without overwriting existing state and apply the selected Git tracking policy. Preserve archived state and other private notes in their existing locations. Keep `config.md` active when archiving completed goals.

## Karpathy guardrails

- Think before coding.
- Prefer simple, working vertical slices.
- Avoid speculative abstractions.
- Make surgical changes in existing codebases.
- Preserve existing behavior unless the user asks otherwise.
- Verify against a concrete goal.

## State visibility policy

Default collaborative mode:

- Commit `.checkpoint-karpathy/config.md`.
- Commit `.checkpoint-karpathy/roadmap.md`.
- Commit `.checkpoint-karpathy/progress.md`.
- Ignore `.checkpoint-karpathy/private/`.

Privacy mode:

- If the user asks to keep planning private, place `config.md`, `roadmap.md`, and `progress.md` inside `.checkpoint-karpathy/private/`.
- Keep configuration, roadmap, and progress untracked in privacy mode; include removal of any formerly tracked active state paths in the next relevant commit.
- Because `.checkpoint-karpathy/private/` is gitignored, all planning state stays private.

Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential business strategy into committed roadmap/progress files.

Use `.checkpoint-karpathy/private/` for sensitive local notes. It must be gitignored.

## Gitignore

Both collaborative and privacy mode use the same single entry:

```gitignore
.checkpoint-karpathy/private/
```

In privacy mode, `config.md`, `roadmap.md`, and `progress.md` are inside `.checkpoint-karpathy/private/`, so they are covered by the same rule.

Do not ignore `.checkpoint-karpathy/` wholesale.

## Git safety

Before staging:

```bash
git status
git diff
```

After staging:

```bash
git diff --staged
```

Stage only relevant files. Do not commit unrelated user changes.

Use the commit message style recorded in `config.md`:

Conventional Commits (default):
```text
type(scope): <summary>
```

Phase-style (optional):
```text
Phase X.Y: <description>
```

Description defaults to English; use another language only when the user asks. Do not commit unrelated user changes.

Do not run destructive Git commands without explicit permission.


## Claude Code usage

When asked to use this workflow, follow the local `CLAUDE.md` and the skill at `.claude/skills/checkpoint-karpathy-development/SKILL.md` if present.

A typical command is:

```text
/checkpoint-karpathy Continue this project using checkpoint-karpathy development. Select the work mode, update the roadmap, complete one subphase, update progress, verify, and commit.
```

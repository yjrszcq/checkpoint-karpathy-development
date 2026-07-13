# Claude Code Instructions: Checkpoint Karpathy Agent Workflow

Use checkpoint-karpathy development for multi-step software work in this project.

## Core behavior

When the user gives a concrete development goal:

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

- **First-time planning:** The roadmap must cover every milestone and subphase needed to achieve all goals. It may be updated later if unexpected situations arise.
- **During execution:** Every development-related conversation must use this skill until the roadmap is complete. A conversation may naturally end (session limit, quota) between subphases — the skill remains active, and the next development conversation should automatically resume from the next unfinished subphase.
- **After completion:** When every subphase and milestone review is done, the skill is no longer active. Do not invoke it again unless the user explicitly asks for checkpoint-karpathy development on a new goal.
- **Re-invocation:** When the user asks to use this skill for a new goal, or when a new conversation continues an unfinished roadmap:
  - If no roadmap exists, this is first-time use — plan from scratch.
  - If the roadmap is already complete, archive `roadmap.md` and `progress.md` to `.checkpoint-karpathy/archive/YYYY-MM-DD-<summary>/` (or `.checkpoint-karpathy/private/archive/YYYY-MM-DD-<summary>/` in privacy mode), then create fresh roadmap and progress files for the new goal.
  - If the roadmap is not yet complete, resume from the next unfinished subphase.

## Karpathy guardrails

- Think before coding.
- Prefer simple, working vertical slices.
- Avoid speculative abstractions.
- Make surgical changes in existing codebases.
- Preserve existing behavior unless the user asks otherwise.
- Verify against a concrete goal.

## State visibility policy

Default collaborative mode:

- Commit `.checkpoint-karpathy/roadmap.md`.
- Commit `.checkpoint-karpathy/progress.md`.
- Ignore `.checkpoint-karpathy/private/`.

Privacy mode:

- If the user asks to keep planning private, place `roadmap.md` and `progress.md` inside `.checkpoint-karpathy/private/`.
- Do not commit roadmap or progress in privacy mode.
- Because `.checkpoint-karpathy/private/` is gitignored, all planning state stays private.

Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential business strategy into committed roadmap/progress files.

Use `.checkpoint-karpathy/private/` for sensitive local notes. It must be gitignored.

## Gitignore

Both collaborative and privacy mode use the same single entry:

```gitignore
.checkpoint-karpathy/private/
```

In privacy mode, `roadmap.md` and `progress.md` are inside `.checkpoint-karpathy/private/`, so they are covered by the same rule.

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

Commit messages — pick one style and stay consistent:

Phase-style (default for roadmap-driven work):
```text
Phase X.Y: <description>
```

Professional-style (Conventional Commits):
```text
type(scope): <English summary>
```

Description defaults to English; use another language only when the user asks. Do not commit unrelated user changes.

Do not run destructive Git commands without explicit permission.


## Claude Code usage

When asked to use this workflow, follow the local `CLAUDE.md` and the skill at `.claude/skills/checkpoint-karpathy-development/SKILL.md` if present.

A typical command is:

```text
/checkpoint-karpathy Continue this project using checkpoint-karpathy development. Select the work mode, update the roadmap, complete one subphase, update progress, verify, and commit.
```

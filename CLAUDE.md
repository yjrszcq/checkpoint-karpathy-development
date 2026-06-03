# Claude Code Instructions: Checkpoint Karpathy Agent Workflow

Use checkpoint-karpathy development for multi-step software work in this project.

## Core behavior

When the user gives a concrete development goal:

1. Select the work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
2. Create or update `.checkpoint-karpathy/roadmap.md`.
3. Split the goal into major milestones and commit-sized subphases.
4. Work on one subphase at a time.
5. Run the smallest project-appropriate verification for normal subphases.
6. Update `.checkpoint-karpathy/progress.md` after each completed subphase.
7. Commit each completed subphase.
8. When a major milestone is complete, perform a standalone milestone review checkpoint before moving on. Do not increment the planned Phase/Subphase number for this closeout; confirm scope, simplify milestone work, run the broadest relevant verification, review for regressions or integration gaps, debug and fix in-scope issues, rerun verification, record progress, and commit the closeout.
9. Keep following the roadmap unless reality changes; if it changes, update the roadmap and record why.

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

- If the user asks to keep planning private, add roadmap/progress to `.gitignore`.
- Do not commit `.checkpoint-karpathy/roadmap.md` or `.checkpoint-karpathy/progress.md` in privacy mode.

Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential business strategy into committed roadmap/progress files.

Use `.checkpoint-karpathy/private/` for sensitive local notes. It must be gitignored.

## Gitignore

Default collaborative mode should ignore only:

```gitignore
.checkpoint-karpathy/private/
```

Privacy mode should ignore:

```gitignore
.checkpoint-karpathy/roadmap.md
.checkpoint-karpathy/progress.md
.checkpoint-karpathy/private/
```

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

Do not run destructive Git commands without explicit permission.


## Claude Code usage

When asked to use this workflow, follow the local `CLAUDE.md` and the skill at `.claude/skills/checkpoint-karpathy-development/SKILL.md` if present.

A typical command is:

```text
/checkpoint-karpathy Continue this project using checkpoint-karpathy development. Select the work mode, update the roadmap, complete one subphase, update progress, verify, and commit.
```

# Checkpoint Karpathy Agent Workflow

Use checkpoint-karpathy development for multi-step software work in this project.

## Core behavior

When the user gives a concrete development goal:

1. Select the work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
2. Create or update `.checkpoint-karpathy/roadmap.md`.
3. Split the goal into major milestones and commit-sized subphases.
4. Work on one subphase at a time.
5. Update `.checkpoint-karpathy/progress.md` after each completed subphase.
6. Run the smallest project-appropriate verification.
7. Commit each completed subphase.
8. Keep following the roadmap unless reality changes; if it changes, update the roadmap and record why.

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

## No workflow scratch directory

Do not create or rely on `.checkpoint-karpathy/tmp/` or any other workflow-specific project-local scratch directory unless the user explicitly asks.

Agent-owned temporary files should use the agent/tool's native temporary storage.

Do not move or redirect project build outputs, runtime temp files, caches, generated files, dependency files, logs, coverage, tests, manifests, lockfiles, source files, configs, migrations, or required build outputs into a workflow directory.

Respect the project's existing build, run, and test output conventions.

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

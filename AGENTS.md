# AGENTS.md

Use checkpoint-karpathy development for this project.

This project should be developed, continued, modified, refactored, and maintained in small, recoverable phases. Each meaningful phase must produce a coherent repository state, update persistent progress notes, run appropriate verification, and create a Git commit.

This rule applies to:

- starting from zero,
- continuing an existing project,
- adding features,
- fixing bugs,
- refactoring,
- late-stage maintenance,
- release preparation,
- documentation and configuration changes that affect development.

## Main Workflow

For multi-step coding work:

1. Select the work mode: greenfield, continuation, feature, bug fix, refactor, or maintenance.
2. Define a small, concrete phase goal.
3. Think before coding: identify assumptions, risks, and the smallest useful vertical slice.
4. Inspect current repository state and `git status` before editing.
5. Implement the minimal coherent change.
6. Avoid speculative abstractions and unrelated refactors.
7. Detect the project stack before choosing verification commands.
8. Prefer project-declared commands over generic language defaults.
9. Run the smallest relevant verification.
10. Update `docs/progress.md`.
11. Keep scratch/intermediate files under `.agent-artifacts/`.
12. Ensure `.agent-artifacts/` is listed in `.gitignore`.
13. Review Git state with `git status`, `git diff`, and `git diff --staged`.
14. Commit the completed phase.

Do not leave completed phase work uncommitted.

## Work Modes

### Greenfield

For empty or new projects, create the minimum coherent project structure for the current phase. Do not build broad unfinished architecture.

### Continuation

For existing projects or partially completed work, first inspect docs, manifests, Git status, and `docs/progress.md` if present. Do not overwrite or discard existing work.

### Feature

Add one useful vertical slice at a time. Preserve existing behavior and commit each completed slice.

### Bug Fix

Reproduce or characterize the bug when possible. Fix the smallest cause. Verify the fix. Document cause, fix, and verification.

### Refactor

Preserve behavior. Avoid API, data format, CLI, config, or workflow breakage unless explicitly requested. Verification is mandatory.

### Maintenance

Be conservative. Prefer small, low-risk changes. Document compatibility and risk notes.

## Engineering Guardrails

Follow these Karpathy-inspired principles:

- Think before coding; do not hide confusion or assumptions.
- Simplicity first; use the minimum code that solves the current phase.
- Surgical changes in existing codebases; touch only what the task requires.
- Goal-driven execution; every phase needs a verifiable success condition.

For greenfield development, create the minimum coherent project structure required for the current phase.

For existing projects, preserve current behavior and match existing style unless instructed otherwise.

## Language and Stack Neutrality

Do not assume Python, Node, Rust, Go, Java, C++, or any other stack unless the repository or user request indicates it.

Before running checks, infer the stack from:

- project docs,
- manifests,
- lockfiles,
- build files,
- test configuration,
- existing scripts.

Prefer project-declared commands over generic language defaults.

If no reliable check command exists, document that honestly in `docs/progress.md`.

## Progress Log

Persistent progress belongs in:

```text
docs/progress.md
```

Each phase entry should include:

- work mode,
- goal,
- completed work,
- files changed,
- verification,
- decisions,
- compatibility or risk notes,
- known issues,
- next step.

The progress log must be useful to a future agent with no access to the previous conversation.

## Intermediate Files

All scratch or intermediate agent outputs belong under:

```text
.agent-artifacts/
```

Examples:

- temporary notes,
- investigation logs,
- generated comparison files,
- throwaway scripts,
- local transcripts,
- screenshots used for analysis,
- experimental outputs,
- draft plans not meant for the repository.

Ensure `.gitignore` contains:

```gitignore
# Agent scratch/intermediate outputs
.agent-artifacts/
```

Do not stage or commit `.agent-artifacts/`.

If an intermediate artifact becomes a real deliverable, move it out of `.agent-artifacts/`, document why in `docs/progress.md`, and commit it as a normal project file.

## Git Rules

Before staging:

```bash
git status
git diff
```

After staging:

```bash
git diff --staged
```

Commit message format:

```text
phase N: <short summary>
```

Do not commit unrelated user changes.

Do not run destructive Git commands without explicit permission, including:

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

Do not commit secrets or generated dependency folders unless the project intentionally tracks them.

## Quota Safety

If the work is large or the session may end soon:

1. Stop expanding scope.
2. Bring current work to a coherent checkpoint if possible.
3. Update `docs/progress.md`.
4. Run the smallest relevant verification.
5. Commit.
6. Report what remains.

Never keep large completed work uncommitted.

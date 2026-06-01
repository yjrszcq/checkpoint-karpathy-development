# CLAUDE.md

Use checkpoint-karpathy development for this project.

Claude Code should treat this file as durable project guidance. For multi-step coding work, use the checkpoint workflow below and the local skill at `.claude/skills/checkpoint-karpathy-development/SKILL.md` when available.

## Default Workflow

For development, continuation, feature work, bug fixing, refactoring, maintenance, release prep, documentation/configuration changes that affect development, or any task where losing progress would be costly:

1. Select the work mode: greenfield, continuation, feature, bug fix, refactor, or maintenance.
2. Define a small, concrete phase goal.
3. Think before coding: identify assumptions, risks, and the smallest useful vertical slice.
4. Inspect repository state before editing, including `git status`.
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

A phase is not complete until it is documented, verified or honestly marked as unverifiable, and committed.

## Work Modes

### Greenfield

For empty or new projects, create the minimum coherent project structure for the current phase. Do not build broad unfinished architecture.

### Continuation

For existing projects or partially completed work, inspect docs, manifests, Git status, and `docs/progress.md` if present. Do not overwrite or discard existing work.

### Feature

Add one useful vertical slice at a time. Preserve existing behavior and commit each completed slice.

### Bug Fix

Reproduce or characterize the bug when possible. Fix the smallest cause. Verify the fix. Document cause, fix, and verification.

### Refactor

Preserve behavior. Avoid API, data format, CLI, config, or workflow breakage unless explicitly requested. Verification is mandatory.

### Maintenance

Be conservative. Prefer small, low-risk changes. Document compatibility and risk notes.

## Karpathy-Inspired Guardrails

- Think before coding; do not hide confusion or assumptions.
- Simplicity first; use the minimum code that solves the current phase.
- Surgical changes in existing codebases; touch only what the task requires.
- Goal-driven execution; every phase needs a verifiable success condition.

For greenfield development, create the minimum coherent project structure required for the current phase.

For existing projects, preserve current behavior and match existing style unless instructed otherwise.

## Language and Stack Neutrality

Do not assume Python, Node, Rust, Go, Java, C++, or any other stack unless the repository or user request indicates it.

Before running checks, inspect project docs, manifests, lockfiles, build files, and existing scripts.

Prefer project-declared commands over generic defaults.

If no reliable check exists, record this in `docs/progress.md` instead of pretending a check passed.

## Intermediate Artifacts

Use `.agent-artifacts/` for scratch files, temporary analysis outputs, generated notes, draft plans, logs, and other intermediate files that should not be committed.

Ensure `.agent-artifacts/` is ignored by Git:

```gitignore
.agent-artifacts/
```

Durable progress belongs in `docs/progress.md`, not in `.agent-artifacts/`.

If an intermediate artifact becomes a real project deliverable, move it out of `.agent-artifacts/`, document the decision in `docs/progress.md`, and then commit it.

## Git Safety

Do not run destructive Git commands without explicit permission.

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

## Claude Code Usage

When starting a large task, the user may invoke:

```text
/checkpoint-karpathy <task>
```

or ask directly:

```text
Use checkpoint-karpathy development for this task.
```

Either way, follow this file and the local skill if installed.

---
name: checkpoint-karpathy-development
description: "Use this skill for roadmap-driven, checkpointed software work across greenfield development, continuation, feature work, bug fixing, refactoring, and maintenance, while following Karpathy-inspired engineering guardrails."
---

# Checkpoint Karpathy Development

Use this skill for software work that may span more than one step or may be interrupted by quota limits, session limits, or context loss.

This workflow combines two ideas:

1. **Roadmap-driven checkpointing** — plan the requested work in `.checkpoint-karpathy/roadmap.md`, split it into major milestones and commit-sized subphases, update `.checkpoint-karpathy/progress.md`, verify each completed subphase, and commit it.
2. **Karpathy-inspired engineering guardrails** — think before coding, keep the solution simple, make surgical changes in existing codebases, and verify against a concrete goal.

The workflow is not limited to starting from zero. It applies to:

- greenfield development,
- mid-project continuation,
- feature development,
- bug fixing,
- refactoring,
- late-stage maintenance,
- release preparation,
- documentation or configuration changes that affect development.

---

## State Files

Use this namespaced directory for durable workflow state:

```text
.checkpoint-karpathy/
  roadmap.md
  progress.md
  private/
```

### Default collaborative mode

By default:

- commit `.checkpoint-karpathy/roadmap.md`,
- commit `.checkpoint-karpathy/progress.md`,
- ignore `.checkpoint-karpathy/private/`.

Rationale: roadmap and progress make the work recoverable across sessions and help collaborators understand direction and status.

### Privacy mode

If the user asks to keep agent planning private, switch to privacy mode:

- add `.checkpoint-karpathy/roadmap.md` to `.gitignore`,
- add `.checkpoint-karpathy/progress.md` to `.gitignore`,
- keep `.checkpoint-karpathy/private/` ignored,
- do not commit roadmap or progress.

Use privacy mode for public repositories or sensitive planning where the user does not want to expose development direction, vulnerability notes, business strategy, or unfinished reasoning.

### Private notes

Put sensitive or non-public notes in:

```text
.checkpoint-karpathy/private/
```

This directory must be ignored by Git.

Do not put secrets, credentials, private customer data, or sensitive vulnerability details into committed roadmap or progress files.

---

## No Workflow Scratch Directory

Do not create or rely on a workflow-specific scratch directory such as `.checkpoint-karpathy/tmp/`.

Agent-owned temporary files should use the agent/tool's own native temporary storage when available.

Do not invent a project-local scratch directory unless the user explicitly asks for one.

Most importantly: do not change where the project itself writes build outputs, runtime temporary files, caches, generated files, logs, coverage reports, test artifacts, dependency files, manifests, lockfiles, or source files just to fit this workflow.

Respect the project's existing conventions for:

- build output,
- cache location,
- generated code,
- runtime temporary files,
- logs,
- coverage,
- test artifacts,
- dependency manifests and lockfiles.

Project files belong in the real project tree. This includes, but is not limited to:

- `go.mod`, `go.sum`,
- `package.json`, lockfiles,
- `Cargo.toml`, `Cargo.lock`,
- `pyproject.toml`, dependency files,
- `pom.xml`, `build.gradle`,
- `Makefile`, `CMakeLists.txt`,
- `Dockerfile`, compose files,
- source files,
- tests,
- configs,
- migrations,
- fixtures required by tests,
- generated files required by the project.

If a project command naturally writes files to a conventional location, do not redirect it unless the project docs or the user explicitly says to do so.

---

## Karpathy-Inspired Guardrails

### Think Before Coding

Before meaningful edits, identify:

- the current work mode,
- the concrete goal,
- the smallest coherent phase,
- assumptions,
- risks,
- verification method.

For clear, low-risk tasks, proceed directly. For ambiguous or high-risk tasks, briefly restate the plan first.

### Simplicity First

Prefer the simplest thing that works.

Avoid:

- speculative abstractions,
- unused frameworks,
- unnecessary layers,
- broad rewrites,
- premature generalization.

A small working vertical slice beats a large unfinished architecture.

### Surgical Changes

For existing codebases:

- touch only relevant files,
- preserve behavior unless the user requested a change,
- avoid unrelated refactors,
- match existing style,
- do not commit unrelated user changes.

For greenfield projects:

- create the minimum coherent structure needed for the current phase,
- do not scaffold large unused systems,
- make each subphase runnable or inspectable.

### Goal-Driven Execution

Every subphase must have:

- a goal,
- a completion condition,
- a verification method,
- a commit.

---

## Work Mode Selection

At the start of a concrete development request, determine the current work mode.

Use one of these modes:

1. **Greenfield Development** — empty or near-empty repository.
2. **Mid-Project Continuation** — existing codebase with ongoing work.
3. **Feature Development** — add a new capability.
4. **Bug Fixing** — reproduce, isolate, fix, and verify a defect.
5. **Refactoring** — change structure while preserving behavior.
6. **Late-Stage Maintenance** — small, careful changes near release or in mature code.

Record the selected mode in `.checkpoint-karpathy/roadmap.md` or `.checkpoint-karpathy/progress.md`.

---

## Roadmap Requirement

When the user first gives a concrete development goal for the current task, create or update:

```text
.checkpoint-karpathy/roadmap.md
```

The roadmap must estimate from the current repository state:

- how many major milestones are needed,
- which commit-sized subphases belong to each milestone,
- what each subphase will change,
- what each subphase's success criteria are,
- how each subphase will be verified,
- likely risks or blockers,
- which subphase should be done next.

Roadmaps are plans, not contracts. They may be updated when reality changes.

Update the roadmap when:

- requirements change,
- a major bug appears,
- a blocker invalidates the plan,
- the project structure differs from assumptions,
- a subphase needs to be split or merged,
- the user changes priority.

If the roadmap changes, record why.

---

## Roadmap Template

Use this structure:

```md
# Checkpoint Karpathy Roadmap

## Goal
<The user's concrete development goal.>

## Work Mode
<greenfield | continuation | feature | bugfix | refactor | maintenance>

## Current State
<Short summary of what exists now.>

## Assumptions
- <Assumption>

## Major Milestones

### Milestone 1: <title>
Purpose: <why this milestone exists>

Subphases:
- [ ] 1.1 <commit-sized goal>
  - Scope: <what will change>
  - Success criteria: <how to know it is done>
  - Verification: <project-appropriate check>
  - Commit target: `phase 1.1: <summary>`

- [ ] 1.2 <commit-sized goal>
  - Scope: <what will change>
  - Success criteria: <how to know it is done>
  - Verification: <project-appropriate check>
  - Commit target: `phase 1.2: <summary>`

### Milestone 2: <title>
Purpose: <why this milestone exists>

Subphases:
- [ ] 2.1 <commit-sized goal>
  - Scope: <what will change>
  - Success criteria: <how to know it is done>
  - Verification: <project-appropriate check>
  - Commit target: `phase 2.1: <summary>`

## Risks / Blockers
- <Risk or blocker>

## Next Subphase
<The next subphase to execute.>

## Roadmap Change Log
- <YYYY-MM-DD>: Initial roadmap created.
```

---

## Progress Log Requirement

After each completed subphase, update:

```text
.checkpoint-karpathy/progress.md
```

Use this structure:

```md
# Checkpoint Karpathy Progress

## Phase <N or M.S>: <short title>

Date: <YYYY-MM-DD>
Roadmap item: <milestone/subphase reference>
Commit: <hash after commit, or pending before commit>

### Goal
<What this phase was meant to accomplish.>

### Completed
- <Concrete completed item>

### Files Changed
- `<path>` — <why it changed>

### Verification
- `<command or method>` — <result>
- If not run: <reason>

### Decisions
- <Important technical decision and rationale>

### Known Issues
- <Open issue, limitation, or risk>
- If none: None known.

### Next Step
<The next roadmap subphase or a roadmap update.>
```

Append entries. Do not erase useful prior history.

---

## Phase Workflow

For each subphase:

1. Select the next roadmap subphase.
2. State the subphase goal briefly.
3. Inspect the repository and project instructions.
4. Make the smallest coherent change that completes the subphase.
5. Detect the project stack before choosing verification.
6. Run the smallest relevant verification.
7. Update `.checkpoint-karpathy/progress.md`.
8. Update `.checkpoint-karpathy/roadmap.md` if the plan changed or the item is complete.
9. Run `git status`.
10. Review relevant diffs with `git diff`.
11. Stage only relevant files.
12. Review staged diff with `git diff --staged`.
13. Commit the completed subphase.
14. Report the commit and next subphase.

A normal commit should correspond to one completed roadmap subphase.

If special circumstances arise, create a temporary checkpoint for the immediate coherent goal, such as:

- roadmap update after requirement change,
- documentation update needed before coding,
- blocker investigation,
- urgent bug fix discovered during development,
- plan correction after repository inspection.

After such a checkpoint, return to the roadmap.

---

## Stack-Neutral Verification

Never assume the project stack.

Before running checks, inspect:

- `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, docs,
- `package.json`, lockfiles,
- `pyproject.toml`, Python config files,
- `Cargo.toml`,
- `go.mod`,
- `pom.xml`, `build.gradle`,
- `.csproj`, `.sln`,
- `CMakeLists.txt`, `Makefile`, `meson.build`,
- `Gemfile`,
- `composer.json`,
- `Package.swift`,
- `Dockerfile`, compose files,
- `justfile`, `Taskfile.yml`.

Prefer project-declared commands over generic guesses.

Use the smallest relevant check:

- test,
- build,
- type check,
- lint,
- format check,
- compile check,
- smoke check,
- manual inspection if no command exists.

If no reliable verification exists yet, write that explicitly in progress.

Do not pretend a check passed.

---

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

Stage only relevant files.

Do not commit unrelated user changes.

Commit message style:

```text
phase 1.1: initialize project skeleton
phase 1.2: add first runnable command
phase 2.1: implement core data model
checkpoint: update roadmap after requirement change
fix: repair blocking test failure before next roadmap phase
```

Do not run destructive Git commands unless the user explicitly asks.

Avoid without explicit permission:

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

If Git is not initialized and the user requested checkpointed development, initialize it:

```bash
git init
```

If commit fails because Git identity is missing, do not fabricate identity. Report the issue and tell the user to configure Git identity.

---

## Gitignore Policy

Default collaborative mode `.gitignore` entry:

```gitignore
.checkpoint-karpathy/private/
```

Privacy mode `.gitignore` entries:

```gitignore
.checkpoint-karpathy/roadmap.md
.checkpoint-karpathy/progress.md
.checkpoint-karpathy/private/
```

Do not add `.checkpoint-karpathy/` wholesale to `.gitignore`, because that would hide roadmap and progress even in collaborative mode.

---

## Final Definition of Done

A subphase is done only when:

- its roadmap item is complete or intentionally adjusted,
- code/project files are coherent,
- verification was run or honestly documented as unavailable,
- `.checkpoint-karpathy/progress.md` is updated,
- `.checkpoint-karpathy/roadmap.md` is updated if needed,
- relevant changes are committed,
- no unrelated user changes were committed,
- the next step is recorded.

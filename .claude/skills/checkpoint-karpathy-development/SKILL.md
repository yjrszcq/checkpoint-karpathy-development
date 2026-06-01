---
name: checkpoint-karpathy-development
description: Use this skill for greenfield development, mid-project continuation, feature work, bug fixing, refactoring, or late-stage maintenance where work must be split into recoverable Git checkpoints while following Karpathy-inspired engineering guardrails: think before coding, simplicity first, surgical changes, and goal-driven verification.
---

# Checkpoint + Karpathy Development

Use this skill for any multi-step coding task where progress must survive quota limits, session interruptions, or context loss.

This skill is not limited to starting projects from zero. It supports:

- **Greenfield development** — starting a new project or module.
- **Mid-project continuation** — continuing existing unfinished work.
- **Feature development** — adding a new capability to an existing project.
- **Bug fixing** — diagnosing and fixing broken behavior.
- **Refactoring** — simplifying internals while preserving behavior.
- **Late-stage maintenance** — small, careful changes to mature code.

This skill combines two concerns:

1. **Checkpoint-driven workflow** — every meaningful phase ends with progress notes, verification, and a Git commit.
2. **Karpathy-inspired engineering guardrails** — think before coding, keep the solution simple, avoid unrelated edits, and verify against explicit goals.

The checkpoint workflow is mandatory. The engineering guardrails shape how each phase is implemented.

---

## Non-Negotiable Outcome

Every completed phase must end with:

- a coherent repository state,
- updated `docs/progress.md`,
- intermediate/scratch artifacts kept under `.agent-artifacts/`,
- `.agent-artifacts/` ignored by Git,
- project-appropriate verification,
- and a Git commit.

A phase is not complete until it is committed.

---

## Work Mode Selection

Before starting, classify the task into one work mode. The mode determines what the first phase should do.

### Mode A: Greenfield Development

Use when the repository is empty, nearly empty, or the user asks to build from zero.

First phase should:

- identify the requested product/project type,
- create only the minimum coherent project skeleton,
- create or update `.gitignore`,
- create `docs/progress.md`,
- initialize Git if needed,
- run the smallest available smoke check,
- commit the skeleton.

Do not create broad speculative architecture.

### Mode B: Mid-Project Continuation

Use when the project already has files and the user wants to continue development.

First phase should:

- inspect existing structure, manifests, docs, and Git status,
- read existing `docs/progress.md` if present,
- infer the current implementation state,
- identify unfinished work and risks,
- avoid overwriting or discarding existing work,
- create a continuation checkpoint before large edits if the working tree is already dirty.

If uncommitted changes exist, determine whether they are relevant. Do not commit unrelated user changes.

### Mode C: Feature Development

Use when adding a new feature to an existing project.

Each phase should:

- choose one vertical slice of the feature,
- preserve existing behavior,
- avoid unrelated refactors,
- add or update focused verification,
- update progress notes,
- commit only relevant files.

### Mode D: Bug Fixing

Use when fixing broken behavior.

Each phase should:

- reproduce or characterize the bug when possible,
- identify the smallest cause,
- make the smallest fix,
- verify the fix using an existing or focused check,
- document the bug, cause, fix, and verification in `docs/progress.md`,
- commit the fix.

Do not rewrite large areas unless the bug cannot be fixed safely otherwise.

### Mode E: Refactoring

Use when restructuring or simplifying code without intended behavior changes.

Each phase should:

- define the behavior that must remain unchanged,
- identify the smallest refactor slice,
- avoid API or data format breakage unless explicitly requested,
- run regression checks,
- document compatibility assumptions,
- commit the refactor.

A refactor without verification is not complete.

### Mode F: Late-Stage Maintenance

Use for mature projects, production code, release preparation, compatibility work, documentation corrections, dependency hygiene, or small hardening changes.

Each phase should:

- be especially conservative,
- preserve documented behavior,
- avoid changing public APIs, CLI flags, config formats, file formats, database schema, or user workflows unless explicitly requested,
- document risk and compatibility impact,
- run the smallest relevant check,
- commit the change.

---

## Core Engineering Guardrails

### 1. Think Before Coding

Do not assume. Do not hide confusion.

Before implementing a non-trivial phase:

- state the phase goal,
- identify assumptions,
- identify what could break,
- choose the smallest useful slice.

For simple, low-risk tasks, internalize this and proceed directly.

### 2. Simplicity First

Use the minimum code and structure that solves the current phase.

Avoid:

- speculative abstractions,
- unused frameworks,
- premature plugin systems,
- unnecessary dependency additions,
- broad architecture for hypothetical future needs.

Prefer a small working vertical slice over a large unfinished system.

### 3. Surgical Changes Where Code Already Exists

For existing codebases:

- touch only files relevant to the phase,
- preserve existing style,
- avoid unrelated refactors,
- do not reformat unrelated files,
- do not mix cleanup with feature or bug-fix work unless necessary.

For greenfield projects, “surgical” means: create the minimum coherent structure required for the current slice.

### 4. Goal-Driven Execution

Every phase must have a success condition.

Examples:

- command runs,
- test passes,
- build completes,
- UI path renders,
- API endpoint responds,
- bug reproduction no longer fails,
- documentation accurately describes the current state.

If no automated check exists, record the manual or smoke verification honestly.

---

## Artifact and Scratch File Rules

Persistent project documentation belongs in:

```text
 docs/progress.md
```

Intermediate or scratch outputs must go under:

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

Ensure `.agent-artifacts/` is ignored by Git.

If `.gitignore` exists, add:

```gitignore
# Agent scratch/intermediate outputs
.agent-artifacts/
```

If `.gitignore` does not exist, create it with that entry. Add stack-specific ignore rules only when the stack is detected from project files or requested by the user.

Do not stage or commit `.agent-artifacts/`.

If an intermediate artifact becomes a real deliverable, move it out of `.agent-artifacts/`, document why in `docs/progress.md`, and then commit it as a normal project file.

---

## Language and Stack Neutrality

Never assume the project is Python, JavaScript, TypeScript, Rust, Go, Java, C++, or any other stack.

Before running checks, detect the project type from existing files.

Inspect project instructions:

```text
README.md
AGENTS.md
CONTRIBUTING.md
docs/
```

Inspect manifests and build files:

```text
package.json
pnpm-lock.yaml
yarn.lock
bun.lockb
deno.json
pyproject.toml
requirements.txt
setup.py
tox.ini
pytest.ini
Cargo.toml
go.mod
pom.xml
build.gradle
settings.gradle
*.csproj
*.sln
CMakeLists.txt
Makefile
meson.build
configure
Gemfile
composer.json
Package.swift
Dockerfile
compose.yaml
docker-compose.yml
justfile
Taskfile.yml
```

Prefer project-declared commands over generic language defaults.

Do not invent a language-specific command when the repository does not indicate that stack.

---

## Phase Workflow

For every phase, follow this workflow.

### Step 1: Select Work Mode

Classify the task as greenfield, mid-project continuation, feature development, bug fixing, refactoring, or late-stage maintenance.

If the mode is ambiguous, choose the safest mode based on the repository state:

- empty repo: greenfield,
- existing repo with unfinished work: continuation,
- existing repo with requested new behavior: feature,
- failing behavior: bug fix,
- behavior-preserving internal change: refactor,
- mature/release-sensitive code: maintenance.

### Step 2: Define the Phase Goal

Before editing, identify the current phase goal in one or two sentences.

The goal must be concrete and verifiable.

Good examples:

```text
Phase 1 goal: inspect the existing project, identify the current state, and create a safe continuation checkpoint.
```

```text
Phase 2 goal: implement the first working slice of the requested feature without changing existing behavior.
```

```text
Phase 3 goal: reproduce the reported bug and add a focused failing check if the project has a test setup.
```

Bad examples:

```text
Build the whole app.
```

```text
Make everything production ready.
```

```text
Refactor the architecture.
```

Those are too broad.

### Step 3: Inspect Repository and Git State

Run or inspect as appropriate:

```bash
git status
```

Read relevant docs and manifests before choosing commands.

If the working tree has uncommitted changes:

- identify which changes are relevant,
- avoid overwriting them,
- do not stage unrelated user changes,
- if necessary, create a progress entry describing the dirty state before proceeding.

### Step 4: Implement the Minimal Coherent Slice

Make the smallest coherent change that completes the phase goal.

For greenfield projects, create only the structure needed for the current slice.

For existing projects, preserve current behavior and style.

For bug fixes, fix the narrow cause.

For refactors, preserve behavior.

For maintenance, minimize risk.

### Step 5: Choose Verification

Select verification based on project evidence.

Priority order:

1. Commands documented in `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, or `docs/`.
2. Scripts declared in a manifest, such as `package.json`.
3. Standard build/test tools clearly indicated by manifest files.
4. Existing test runner or build system already present in the repository.
5. A minimal smoke check for the artifact created in this phase.
6. If none exists, document that no project-standard check exists yet.

Use the smallest relevant check for the phase.

Do not run expensive full-suite checks when a smaller check proves the phase, unless project instructions require it.

### Step 6: Run Verification

Run the selected check.

If a check fails:

- determine whether the failure is caused by current phase changes,
- fix it if in scope,
- otherwise record the failure clearly in `docs/progress.md`,
- do not hide it.

If verification cannot run:

- record the reason,
- record what was checked instead.

### Step 7: Update `docs/progress.md`

Create `docs/` if missing.

Create or append to:

```text
docs/progress.md
```

Do not erase useful prior history.

Use this structure:

```md
# Progress Log

## Phase N: <short title>

Date: <YYYY-MM-DD>

### Work Mode
<Greenfield / Continuation / Feature / Bug Fix / Refactor / Maintenance>

### Goal
<What this phase was meant to accomplish.>

### Completed
- <Concrete completed item>
- <Concrete completed item>

### Files Changed
- `<path>` — <why it changed>
- `<path>` — <why it changed>

### Verification
- `<command or method>` — <result>
- If not run: <reason>

### Decisions
- <Important technical decision and rationale>

### Compatibility / Risk Notes
- <Existing behavior, API, data, config, or workflow risk>
- If none: None known.

### Known Issues
- <Open issue, limitation, risk, or failed check>
- If none: None known.

### Next Step
<The next concrete phase to perform.>
```

The progress log must be useful to a future agent with no access to the previous conversation.

### Step 8: Review Git Diff

Before staging:

```bash
git status
git diff
```

After staging:

```bash
git diff --staged
```

Confirm `.agent-artifacts/` is not staged.

Confirm unrelated user changes are not staged.

### Step 9: Commit

If Git is not initialized and the user requested checkpoint-driven work in this repository, initialize Git:

```bash
git init
```

Stage only relevant files:

```bash
git add <relevant files>
```

Prefer explicit paths over `git add .` when unrelated files exist.

Commit with a clear message:

```bash
git commit -m "phase N: <short summary>"
```

Commit message examples:

```text
phase 1: initialize project skeleton
phase 2: inspect existing app state
phase 3: add first feature slice
phase 4: fix login validation bug
phase 5: refactor parser without behavior change
phase 6: harden release configuration
```

If commit fails because Git identity is missing:

- do not fabricate identity,
- leave the progress log updated,
- report the failure,
- tell the user to configure Git identity.

Only suggest configuration commands. Do not set them without explicit user permission.

### Step 10: Report Back

After each phase, report:

```text
Phase N complete.
Mode: <work mode>
Commit: <short hash if available>
Verification: <command/method and result>
Progress log: docs/progress.md
Next: <next phase>
```

Keep the report short.

---

## Git Safety Rules

Never run destructive Git commands unless the user explicitly asks.

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

Do not delete user work.

Do not commit secrets.

Do not commit generated dependency folders unless the project intentionally tracks them.

Usually avoid committing:

```text
node_modules/
venv/
.venv/
dist/
build/
target/
coverage/
.env
.env.local
*.log
.agent-artifacts/
```

Respect `.gitignore`.

---

## Handling Quota or Session Risk

If the task is large or the session may end soon:

1. Stop expanding scope.
2. Bring the current work to a coherent checkpoint if possible.
3. Update `docs/progress.md`.
4. Run the smallest relevant verification.
5. Commit.
6. Report what remains.

Never keep large completed work uncommitted.

If work is incomplete but valuable:

- make it coherent if possible,
- document its incomplete status,
- commit only if it does not leave the project misleadingly broken.

Use a commit message that makes the state clear:

```text
checkpoint: document incomplete investigation
```

Only use this when a normal phase commit is not possible.

---

## Interaction Rules

For clear tasks, proceed directly.

For ambiguous or risky tasks, briefly restate the intended phase plan before editing.

Do not ask unnecessary questions if a safe first phase is obvious.

When the user says the work may exceed quota, prioritize checkpoints over expanding scope.

---

## Relationship to Other Instructions

This skill controls the development workflow.

Project `AGENTS.md` and stack-specific instructions may add details, but they must not override checkpointing unless the user explicitly says so.

Recommended priority:

1. user’s explicit request,
2. checkpoint-karpathy-development workflow,
3. project-specific `AGENTS.md`,
4. stack-specific conventions,
5. general code style or review guidance.

If another instruction encourages large sweeping changes, split those changes into checkpointed phases.

---

## Final Rule

A phase is not done until:

- the code or project files are coherent,
- `docs/progress.md` is updated,
- `.agent-artifacts/` is ignored and not staged,
- verification has been run or honestly documented as unavailable,
- relevant files are committed,
- and the next step is recorded.

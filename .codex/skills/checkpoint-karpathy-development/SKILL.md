---
name: checkpoint-karpathy-development
description: "Use this skill for roadmap-driven, checkpointed software work across greenfield development, continuation, feature work, bug fixing, refactoring, and maintenance, while following Karpathy-inspired engineering guardrails."
---

# Checkpoint Karpathy Development

Use this skill for software work that may span more than one step or may be interrupted by quota limits, session limits, or context loss.

This workflow combines two ideas:

1. **Roadmap-driven checkpointing** — plan the requested work in `.checkpoint-karpathy/roadmap.md`, split it into major milestones and commit-sized subphases, update `.checkpoint-karpathy/progress.md`, verify and commit each completed subphase, then run a standalone milestone review checkpoint before moving on from a completed major milestone.
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

## Skill Lifecycle

### First-Time Planning

When this skill is first invoked for a development goal:

- The roadmap must plan completely from the current state to the full achievement of all stated goals. Every major milestone and subphase needed to reach the end state must be included.
- The agent should state the current defaults: collaborative mode (roadmap and progress are committed) and Phase-style commit messages. Tell the user these can be changed — privacy mode moves roadmap and progress into the gitignored `private/` directory, and Professional-style uses Conventional Commits format.

Roadmaps are plans, not contracts. They may be updated later if unexpected situations arise, requirements change, or blockers appear. But the initial roadmap must be a complete end-to-end plan, not a partial sketch.

### During Execution

Once this skill is active and the roadmap has subphases remaining:

- Every development-related conversation must use this skill until the roadmap is complete. The user does not need to re-invoke it each time.
- When a conversation ends (session limit, quota, or user closes it), the skill itself is not "exited" — the roadmap persists. The next conversation that continues development work should automatically resume this skill from the next unfinished subphase.

### After Roadmap Completion

When every subphase and milestone review in the roadmap is complete, the goal is done:

- The skill is no longer active. Do not invoke it proactively in future conversations.
- Only use this skill again when the user explicitly asks for checkpoint-karpathy development on a new goal.
- Normal development questions or minor edits after completion do not need this skill.

### Re-invocation and Archiving

This procedure applies in two situations: the user explicitly asks to use this skill for a new goal, or a new conversation begins and an unfinished roadmap indicates development should continue.

1. Check whether `.checkpoint-karpathy/roadmap.md` (or `.checkpoint-karpathy/private/roadmap.md` in privacy mode) exists.
2. **No roadmap exists:** This is first-time use. Follow the First-Time Planning procedure.
3. **Roadmap exists and is complete** (all subphases done, all milestone reviews committed):
   - This is a new goal. Archive the current roadmap and progress files before starting fresh.
   - Collaborative mode archive path: `.checkpoint-karpathy/archive/YYYY-MM-DD-<summary>/`
   - Privacy mode archive path: `.checkpoint-karpathy/private/archive/YYYY-MM-DD-<summary>/`
   - `<summary>` is a brief kebab-case label for the completed goal (e.g., `user-auth`). Keep it short — it is a directory name.
   - Move `roadmap.md` and `progress.md` into the archive directory.
   - After archiving, create a fresh `roadmap.md` and `progress.md` for the new goal.
4. **Roadmap exists and is not yet complete:**
   - Resume from the next unfinished subphase.
   - Do not archive or recreate anything.

---

## State Files

Use this namespaced directory for durable workflow state:

**Collaborative mode:**
```text
.checkpoint-karpathy/
  roadmap.md
  progress.md
  private/
  archive/
```

**Privacy mode:**
```text
.checkpoint-karpathy/
  private/
    roadmap.md
    progress.md
    archive/
```

### Default collaborative mode

By default:

- commit `.checkpoint-karpathy/roadmap.md`,
- commit `.checkpoint-karpathy/progress.md`,
- ignore `.checkpoint-karpathy/private/`.

Rationale: roadmap and progress make the work recoverable across sessions and help collaborators understand direction and status.

### Privacy mode

If the user asks to keep agent planning private, switch to privacy mode:

- place `roadmap.md` and `progress.md` inside `.checkpoint-karpathy/private/`,
- keep `.checkpoint-karpathy/private/` ignored by Git,
- do not commit roadmap or progress.

Because `.checkpoint-karpathy/private/` is gitignored, the roadmap and progress files are kept private.

Use privacy mode for public repositories or sensitive planning where the user does not want to expose development direction, vulnerability notes, business strategy, or unfinished reasoning.

### Private notes

Put sensitive or non-public notes in:

```text
.checkpoint-karpathy/private/
```

This directory must be ignored by Git.

In privacy mode, roadmap and progress files live here alongside other private notes.

Do not put secrets, credentials, private customer data, or sensitive vulnerability details into committed roadmap or progress files.

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

Every major milestone must end with a standalone milestone review checkpoint before the agent starts the next milestone or declares the goal done.

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

The roadmap must plan completely from the current repository state to the full achievement of all stated goals:

- how many major milestones are needed,
- which commit-sized subphases belong to each milestone,
- what each subphase will change,
- what each subphase's success criteria are,
- how each subphase will be verified,
- how each major milestone will be reviewed before moving on,
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
  - Commit target: `Phase X.Y: <description>` or `<type>(<scope>): <summary>`

- [ ] 1.2 <commit-sized goal>
  - Scope: <what will change>
  - Success criteria: <how to know it is done>
  - Verification: <project-appropriate check>
  - Commit target: `Phase X.Y: <description>` or `<type>(<scope>): <summary>`

Milestone review:
- Trigger: After the last planned subphase in this milestone is complete.
- Phase label: `Phase 1.2 Milestone Review: <summary>`; this does not increment to `Phase 1.3`.
- Scope: Close out only the work introduced or substantially touched by this milestone.
- Order: confirm scope, simplify, run broad verification, review, debug and fix, rerun verification, record progress, commit.
- Success criteria: No avoidable complexity, unused artifacts, known regressions, unresolved review findings, or failing checks remain.
- Verification: <broadest project-appropriate check for this milestone, plus targeted checks for changed behavior after fixes>
- Commit target: `Phase X.Y Milestone Review: <description>` or `<type>(<scope>): review <English summary>`

### Milestone 2: <title>
Purpose: <why this milestone exists>

Subphases:
- [ ] 2.1 <commit-sized goal>
  - Scope: <what will change>
  - Success criteria: <how to know it is done>
  - Verification: <project-appropriate check>
  - Commit target: `Phase X.Y: <description>` or `<type>(<scope>): <summary>`

Milestone review:
- Trigger: After the last planned subphase in this milestone is complete.
- Phase label: `Phase 2.1 Milestone Review: <summary>`; this does not increment to `Phase 2.2`.
- Scope: Close out only the work introduced or substantially touched by this milestone.
- Order: confirm scope, simplify, run broad verification, review, debug and fix, rerun verification, record progress, commit.
- Success criteria: No avoidable complexity, unused artifacts, known regressions, unresolved review findings, or failing checks remain.
- Verification: <broadest project-appropriate check for this milestone, plus targeted checks for changed behavior after fixes>
- Commit target: `Phase X.Y Milestone Review: <description>` or `<type>(<scope>): review <English summary>`

## Risks / Blockers
- <Risk or blocker>

## Next Subphase
<The next subphase to execute.>

## Roadmap Change Log
- <YYYY-MM-DD>: Initial roadmap created.
```

---

## Milestone Review Requirement

When all planned subphases in a major milestone are complete, perform a standalone milestone review checkpoint before starting the next milestone or declaring the goal done.

The milestone review is separate from the final planned subphase. It must update `.checkpoint-karpathy/progress.md` and have its own commit, but it does not consume or increment the planned Phase/Subphase number. Reuse the last completed planned phase label with a review suffix, such as:

```md
## Phase 1.2 Milestone Review: stabilize authentication flow
```

Do not label this checkpoint as `Phase 1.3` unless `1.3` is an actual planned roadmap subphase.

Use this order for the milestone review:

1. Confirm scope and evidence: restate what the milestone was meant to accomplish and which touched surfaces need review.
2. Simplify: remove speculative abstractions, unnecessary layers, unused frameworks, unused files, unused imports, and dead paths introduced by the milestone.
3. Run broad verification: run the broadest project-appropriate verification available for the milestone's touched surface, plus targeted checks for changed behavior.
4. Review: inspect the whole milestone for regressions, inconsistent behavior, missing tests, stale documentation, roadmap drift, and integration gaps.
5. Debug and fix: reproduce every failing check or discovered defect that is in scope, isolate the cause, and fix it.
6. Rerun verification: rerun the failed checks and the broad milestone verification after fixes.
7. Record and commit: update progress with the review results, update the roadmap if needed, review diffs, and commit the milestone review checkpoint.

Preserve existing behavior unless the user requested a change, and avoid unrelated refactors. Do not mark the milestone complete until simplification, verification results, review findings, debugging, fixes, and final rerun results are recorded in `.checkpoint-karpathy/progress.md`. If a blocking issue cannot be fixed in the review checkpoint, update the roadmap, record the blocker in progress, and commit only a coherent checkpoint that leaves the repository understandable.

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

For a milestone review checkpoint, use a non-incrementing phase label and include:

```md
## Phase <last planned phase> Milestone Review: <short title>

Date: <YYYY-MM-DD>
Roadmap item: Milestone <N> Review after Phase <last planned phase>
Commit: <hash after commit, or pending before commit>

### Goal
<What the milestone review was meant to stabilize.>

### Closeout Order
- Scope and evidence: <confirmed milestone goal and touched surface>
- Simplification: <what was simplified or why no simplification was needed>
- Broad verification: <initial broad checks and results>
- Review findings: <findings and outcomes>
- Debugging / fixes: <bugs found and fixed, or none>
- Final verification rerun: <failed checks and broad checks rerun after fixes>
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
9. If this subphase completes a major milestone, set the next step to the standalone Milestone Review Requirement using the same planned phase label with a review suffix.
10. Run `git status`.
11. Review relevant diffs with `git diff`.
12. Stage only relevant files.
13. Review staged diff with `git diff --staged`.
14. Commit the completed subphase.
15. Report the commit and next subphase.

A normal commit should correspond to one completed roadmap subphase.

For each milestone review checkpoint:

1. Confirm that every planned subphase in the milestone is complete and committed.
2. Use the last planned phase label with a milestone-review suffix; do not increment the planned Phase/Subphase number.
3. Follow the Milestone Review Requirement order through the final verification rerun.
4. Update `.checkpoint-karpathy/progress.md` with the milestone review entry.
5. Update `.checkpoint-karpathy/roadmap.md` to mark the milestone reviewed or to record any blocker.
6. Run `git status`.
7. Review relevant diffs with `git diff`.
8. Stage only relevant files.
9. Review staged diff with `git diff --staged`.
10. Commit the milestone review checkpoint.
11. Report the commit and the next planned subphase or goal completion.

If special circumstances arise, create a temporary checkpoint for the immediate coherent goal, such as:

- roadmap update after requirement change,
- documentation update needed before coding,
- blocker investigation,
- urgent bug fix discovered during development,
- plan correction after repository inspection.

After such a checkpoint, return to the roadmap.

### Lifecycle Behavior During Execution

Within a conversation, while this skill is active and the roadmap has unfinished items:

- After completing a subphase or milestone review, immediately proceed to the next roadmap item.
- Keep executing until this conversation ends or the roadmap is complete.

When the final milestone review is committed and the roadmap is fully complete:

- Report that the goal is complete.
- The skill is no longer active. Do not invoke it again unless the user explicitly asks for checkpoint-karpathy development on a new goal.

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

Commit message style — choose one and stay consistent:

**Phase-style** (default for roadmap-driven work):
```text
Phase X.Y: <description>
```
- Uses the roadmap phase label as the commit subject prefix.
- `<description>` is a concise summary of what changed.
- Description defaults to English; use another language only when the user asks.

**Professional-style** (Conventional Commits):
```text
type(scope): <English summary>
```
- Uses Conventional Commits types and scopes.
- Description defaults to English; use another language only when the user asks.
- Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`, `style`, `revert`.
- Common scopes: `web`, `server`, `docs`, `skill`, `test`, `config`, or omit when forced.
- Examples:
```text
feat(web): add remote login proxy configuration
fix(server): store points count as long
docs(skill): require conventional commit messages
chore(checkpoint): update roadmap after requirement change
test(auth): cover expired session refresh
revert: revert "fix(server): store points count as long"
```

General rules:
- Keep the subject concise, action-oriented, and specific to the completed subphase.
- Do not commit unrelated user changes.

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

Both collaborative mode and privacy mode use the same `.gitignore` entry:

```gitignore
.checkpoint-karpathy/private/
```

In collaborative mode, this keeps the `private/` notes directory out of version control. In privacy mode, `roadmap.md` and `progress.md` are placed inside `.checkpoint-karpathy/private/`, so they are covered by the same rule.

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

A major milestone is done only when:

- every planned subphase in that milestone is complete and committed,
- the standalone milestone review checkpoint is complete and committed,
- progress records the closeout order, findings, fixes, and final verification rerun,
- the next planned subphase or goal completion is recorded.

The full roadmap is complete only when:

- every major milestone and its review checkpoint are done and committed,
- progress records the final milestone review,
- the next step is recorded as goal completion.

After full roadmap completion, the skill is no longer active. Do not invoke it again unless the user explicitly asks for checkpoint-karpathy development on a new goal.

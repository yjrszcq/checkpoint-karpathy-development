---
name: checkpoint-karpathy-development
description: "Use this skill for roadmap-driven, checkpointed software work across greenfield development, continuation, feature work, bug fixing, refactoring, and maintenance, while following Karpathy-inspired engineering guardrails."
---

# Checkpoint Karpathy Development

Use this skill for software work that may span more than one step or may be interrupted by quota limits, session limits, or context loss.

This workflow combines two ideas:

1. **Roadmap-driven checkpointing** — plan the requested work inside the fixed `.checkpoint-karpathy/roadmap/` directory using a compact or structured layout, split it into major milestones and commit-sized subphases, update `roadmap/progress.md`, verify and commit each completed subphase, then run a standalone milestone review checkpoint before moving on from a completed major milestone.
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

## Project Configuration and Initialization

Before each use, look for `config.md` in `.checkpoint-karpathy/` and `.checkpoint-karpathy/private/`.

- Read an existing configuration and use its settings across conversations and goals. Change settings only at the user's request.
- Create it only if missing, before planning. Use each user-specified setting and the default for anything unspecified.
- If both locations contain a configuration, resolve which is active with the user before proceeding.
- Preserve existing planning content when initializing configuration or filling missing settings. Retain recorded values and add only missing settings with their descriptions and defaults.

Generate a configuration that explains every setting, its accepted values, effects, and default. Use the user's language for the explanations. Users edit the `Value` for each setting:

```md
# Checkpoint Karpathy Configuration

## Mode
- Value: collaborative
- Purpose: Select planning visibility and state location.
- Accepted values:
  - collaborative: Track configuration, roadmap documents, and goal archives in Git.
  - privacy: Keep configuration, roadmap documents, and goal archives under Git-ignored private/.
- Default: collaborative

## Commit message style
- Value: conventional
- Purpose: Select commit subject format.
- Accepted values:
  - conventional: Conventional Commits, for example feat(auth): add login.
  - phase: Phase-style, for example Phase 1.1: add login.
- Default: conventional

## Roadmap layout
- Value: auto
- Purpose: Select how a goal's planning documents are organized.
- Accepted values:
  - auto: Let the agent choose and reassess compact or structured layout for the whole goal.
  - compact: Use roadmap/roadmap.md and roadmap/progress.md; switch only at the user's request.
  - structured: Use separate overview, status, context, milestones, changelog, and progress documents in roadmap/; switch only at the user's request.
- Default: auto
```

The state directory is `.checkpoint-karpathy/` in collaborative mode and `.checkpoint-karpathy/private/` in privacy mode. `config.md` sits directly in that directory, alongside the fixed `roadmap/` directory.

During initialization, create the selected state directory and its `roadmap/`, plus `.checkpoint-karpathy/private/work/` in both modes. Reuse existing directories and ensure `.checkpoint-karpathy/private/` is ignored by Git. Create work categories and `archive/` only as needed. An empty `roadmap/` is a directory ready for planning, not an existing goal.

When the user requests settings changes, update only the requested values and apply them to subsequent work. Update uncompleted commit targets for a commit-style change. Apply layout requests using Layout Selection and Switching below.

For a visibility-mode change, create or reuse the destination `roadmap/`, move the active goal contents into it, and move `config.md` into its parent state directory, preserving content and relative links. Check destination conflicts before moving; do not overwrite state. Keep the source `roadmap/` directory in place. Apply the selected Git tracking policy; include removal of formerly tracked active state paths in the next relevant commit when switching to privacy. Existing Git history remains. Archived goals, other private notes, and `private/work/` retain their locations and visibility.

Paths below illustrate collaborative mode. Resolve `config.md`, `roadmap/`, and `archive/` relative to the selected state directory. The work directory always uses `.checkpoint-karpathy/private/work/`.

---

## State Files and Visibility

**Collaborative mode:**

```text
.checkpoint-karpathy/
  config.md
  roadmap/
  private/
    work/
  archive/
```

**Privacy mode:**

```text
.checkpoint-karpathy/
  private/
    config.md
    roadmap/
    work/
    archive/
```

**Compact layout:**

```text
roadmap/
  roadmap.md
  progress.md
```

**Structured layout:**

```text
roadmap/
  README.md
  status.md
  context.md
  milestones.md
  changelog.md
  progress.md
```

In collaborative mode, commit configuration, roadmap contents, and goal archives; ignore `.checkpoint-karpathy/private/`. In privacy mode, keep all state under `private/` untracked. Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential strategy into committed planning documents. Sensitive local notes belong under `private/` in either mode.

### Temporary work files

Use `.checkpoint-karpathy/private/work/` for temporary project files. Create it during initialization in both modes. It stays in place during mode changes, layout switches, and goal archiving. Do not automatically archive or clear its contents when starting a new goal.

Keep the work root free of loose files. Classify by purpose or task, reuse suitable categories, and create only needed subdirectories. Subdivide large categories by task, phase, or run. Examples:

- `logs/`, `checks/`, `verification/`: command output, test logs, and verification evidence.
- `tools/`, `probes/`: temporary scripts and diagnostics.
- `reports/`, `reviews/`, `notes/`: analysis and investigation records.
- `browser/`, `screenshots/`: browser profiles, traces, and screenshots.
- `configs/`, `fixtures/`: temporary configurations and inputs.
- `backups/`, `drafts/`: intermediate copies and drafts.
- `bin/`, `artifacts/`: temporary executables, build output, and profiling data.

A task directory may group its scripts, logs, and reports into subdirectories. Direct tool-created temporary data into work categories where supported. Keep maintained source, tests, and user deliverables in their intended project locations.

Manage temporary content separately, retaining useful tools or evidence and cleaning disposable material as needed under project deletion rules. Record durable conclusions and verification summaries in `roadmap/progress.md` so archived documents explain results without depending only on temporary-file links. Raw evidence may remain in task-specific work directories with its path recorded in progress.

---

## Skill Lifecycle and Completion

On actual first use, initialize configuration and directories, briefly state the selected settings, and proceed without asking the user to choose unspecified settings. For every new goal, plan fully from the current state to all stated goals, including every milestone, commit-sized subphase, and milestone review. Plans may change when evidence or requirements change; record material changes and their reasons.

### Completion state

Record `Completion` in `roadmap/roadmap.md` for compact layout or `roadmap/status.md` for structured layout:

| Value | Meaning |
|---|---|
| `incomplete` (未完成) | The goal remains active and completion conditions are not all met. |
| `completed` (已完成) | All subphases, milestone reviews, commits, and overall acceptance criteria are satisfied with recorded verification evidence. |
| `cancelled` (已取消) | The user explicitly requests or confirms termination of the goal. |

Paused, blocked, and in-progress describe current execution, not additional completion values; keep `incomplete`. Do not infer cancellation from difficulty, inactivity, or blockers. On cancellation, record the reason in the completion document and append a termination entry to progress. Preserve unfinished checkboxes and completed work accurately.

While a goal is `incomplete`, use this workflow across development conversations and resume the next unfinished action without requiring re-invocation. A session ending does not cancel or complete the goal. After `completed` or `cancelled`, deactivate this workflow and leave its documents in place. Use it for a new goal only when the user explicitly invokes it.

### Resume and new goals

1. Read configuration, initialize missing fixed directories, and inspect the actual layout. Read the compact roadmap or the structured overview and status, then recent progress and the relevant plan, dependencies, assumptions, and blockers.
2. If goal documents are absent, select a layout and create a complete plan. Preserve existing content if documents are partial or outside the active directory; organize it without overwriting or treating it as a new goal. Recover missing state from the plan and evidence, and clarify conflicting goals or terminal states rather than guessing.
3. If `incomplete`, resume the next action. Use milestone review or blocker resolution as the next action when appropriate. Check the complete plan before changing scope or cross-milestone dependencies.
4. If `completed`, verify the completion claim against plan checkboxes, review records, and overall acceptance. If inconsistent, reconcile the state before archiving.
5. If `completed` or `cancelled` and starting a new goal, archive the old goal contents as below, select the new goal's layout, and initialize fresh goal documents in the same `roadmap/`. Cancellation does not require unfinished phases to pass acceptance.

### Archiving

Use `archive/YYYYMMDDa-<summary>/` within the selected state directory. The letter increments (`a` … `z`, `aa`, `ab`, …) to avoid same-day collisions. Read the summary from the old goal and use a short kebab-case name describing that completed or cancelled goal.

Create an unused archive destination, then move **all contents** of the active `roadmap/`, including any added subdirectories, directly into it. Check conflicts and preserve relative links within the goal documents. Keep the fixed `roadmap/` directory itself; create new goal files inside it after archiving succeeds.

```text
archive/
  20261026a-linked-market-information/
    README.md
    status.md
    context.md
    milestones.md
    changelog.md
    progress.md
```

For compact layout, that archive directly contains `roadmap.md` and `progress.md`. The archive has no extra enclosing `roadmap/` layer. Keep `config.md` active and reuse it; leave `private/work/` and its contents in place. Archive on the next invocation for a new goal, not immediately upon completion or cancellation.

---

## Layout Selection and Switching

Visibility mode, commit style, and roadmap layout are separate settings.

- `auto`: Choose a layout for each new goal and reassess during execution. The agent may switch in either direction when it improves readability and maintenance.
- `compact`: Use compact layout; switch only when the user requests it.
- `structured`: Use structured layout; switch only when the user requests it.

Judge the **whole goal**, including its complete plan, dependencies, background, design evolution, and accumulated history. Compact fits focused goals with little context and plan history. Structured fits multiple milestones, complex dependencies, or substantial evolving context and history. Remaining task count alone is not a reason to switch; approaching completion does not make a large goal small. Avoid frequent switching with little benefit.

Read existing documents by meaning; headings and wording may differ from the examples. Templates guide organization and should not block recovery of valid user-edited content. Under `auto`, retain `auto` in configuration; the active files identify the actual layout.

### Switching procedure

1. Inspect every goal document and subdirectory. Map all content to the destination layout, preserving goal, acceptance, completion state, stage identifiers, dependencies, reviews, decisions, and all execution and plan-change history.
2. Before edits, copy the full contents of `roadmap/` to a unique `.checkpoint-karpathy/private/work/backups/roadmap-layout/<timestamp>-<source>-to-<target>/` directory. Use this private path in both modes. Put the original files and subdirectories directly in the backup, verify the copy is complete, and do not overwrite a prior backup.
3. Prepare and inspect the target documents, using `private/work/drafts/` if needed. Check destination conflicts. Keep progress history intact; preserve meaning when updating its links. Do not discard custom sections merely because they are absent from a template.
4. Reorganize contents inside the fixed `roadmap/`. Update relative links and anchors; retain stable identifiers. Relocate superseded files individually to a separate subdirectory of the backup rather than leaving conflicting active layouts. Follow project deletion rules.
5. Verify content coverage, completion and phase states, history, links, and the new entry point against the backup. If the conversion fails, preserve the partial result separately and restore the backed-up content before continuing work.
6. Record the reason, source and target layouts, and backup path in the active plan-change log. A layout switch is not a new goal and does not trigger goal archiving. Change configuration only to reflect the user's requested setting.

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

Record the selected work mode in `roadmap/roadmap.md` or `roadmap/README.md`, according to the layout.

---

## Roadmap Documents

Create the entire goal plan inside the selected state directory's fixed `roadmap/`. Read [references/roadmap-templates.md](references/roadmap-templates.md) when creating documents or switching layouts. It provides compact and structured examples plus the milestone and change-entry content.

| Information | Compact | Structured |
|---|---|---|
| Goal, overall acceptance, scope, work mode, initial state, navigation | `roadmap.md` | `README.md` |
| Completion, current snapshot, current phase reference, next action | `roadmap.md` | `status.md` |
| Constraints, assumptions, active risks and blockers, evidence | `roadmap.md` | `context.md` |
| All milestones and subphases, dependencies, scope, acceptance, verification, commit targets, review requirements and completion checkboxes | `roadmap.md` | `milestones.md` |
| Material plan adjustments: reason, change, affected phases, impact, links | Roadmap Change Log in `roadmap.md` | `changelog.md` |
| Actual work, verification results, commits, execution decisions, issue handling | `progress.md` | `progress.md` |

Keep the overview focused on the goal, stable background, and navigation. Keep current status as a latest snapshot, and append execution and plan-change histories. Detailed phase and review completion belongs in the milestone plan; current status references it. Assumption, risk, and blocker details belong in context; current status links to them. Progress entries preserve the execution state at that time; their historical Next Step does not override the current next action.

**Keep roadmap checkboxes current.** As each planned item meets its completion and verification requirements, change its `[ ]` to `[x]` in the active plan: `roadmap/roadmap.md` for compact layout, or `roadmap/milestones.md` (and any split milestone documents) for structured layout. Check off milestone reviews separately after they pass. Update the checkboxes with the corresponding progress entry and include them in the checkpoint commit; a progress entry or status update alone does not mark a plan item complete. Leave unfinished, blocked, or cancelled items unchecked.

Plan completely from the current repository state to all stated goals. Include dependencies, commit-sized subphases with concrete success criteria and verification, a standalone review for every milestone, overall goal acceptance, and the next action. A single subphase or milestone example does not limit the total plan. Preserve stable identifiers and use relative links to connect evidence and plan entries.

Update the active plan when requirements, priorities, assumptions, blockers, or repository evidence invalidate it, or when phases need splitting or merging. Record material changes and their reason and impact in the plan-change log. Ordinary checkbox updates and next-action updates need no plan-change entry. Link execution entries to the change record instead of duplicating explanations.

When a document becomes difficult to read as a whole, split by actual retrieval needs, such as per-milestone documents. Preserve navigation, complete coverage, identifiers, and histories, and include added files in switching and archiving. Keep maintained design documents in their intended project documentation locations and reference them; record the scheduling impact of design changes in the plan-change log.

---

## Milestone Review Requirement

When all planned subphases in a major milestone are complete, perform a standalone milestone review checkpoint before starting the next milestone or declaring the goal done.

The milestone review is separate from the final planned subphase. It must update `.checkpoint-karpathy/roadmap/progress.md` and have its own commit, but it does not consume or increment the planned Phase/Subphase number. Reuse the last completed planned phase label with a review suffix, such as:

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

Preserve existing behavior unless the user requested a change, and avoid unrelated refactors. Do not mark the milestone complete until simplification, verification results, review findings, debugging, fixes, and final rerun results are recorded in `.checkpoint-karpathy/roadmap/progress.md`. If a blocking issue cannot be fixed in the review checkpoint, update the roadmap, record the blocker in progress, and commit only a coherent checkpoint that leaves the repository understandable.

---

## Progress Log Requirement

After each completed subphase, update:

```text
.checkpoint-karpathy/roadmap/progress.md
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
7. Update `.checkpoint-karpathy/roadmap/progress.md`.
8. Update the active milestone plan checkbox from `[ ]` to `[x]` and the current snapshot and Next Action in the completion document. Update context if assumptions, risks, or blockers change; append material plan changes to the plan-change log.
9. If this subphase completes a major milestone, set the next step to the standalone Milestone Review Requirement using the same planned phase label with a review suffix.
10. Run `git status`.
11. Review relevant diffs with `git diff`.
12. Stage only relevant files.
13. Review staged diff with `git diff --staged`.
14. Commit the completed subphase.
15. Report the commit and next action.

A normal commit should correspond to one completed roadmap subphase.

For each milestone review checkpoint:

1. Confirm that every planned subphase in the milestone is complete and committed.
2. Use the last planned phase label with a milestone-review suffix; do not increment the planned Phase/Subphase number.
3. Follow the Milestone Review Requirement order through the final verification rerun.
4. Update `.checkpoint-karpathy/roadmap/progress.md` with the milestone review entry.
5. Mark the milestone review checkbox complete in the active plan after review requirements pass. Update current status and Next Action, keep blocker details in context, and record material plan changes. For the final review, verify overall acceptance and set Completion to `completed` only when the full goal meets the definition of done; include this state in the closeout commit.
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
- Keep executing until this conversation ends, the goal is completed, or the user cancels or pauses work.

When the final milestone review is committed, overall acceptance is verified, and Completion is `completed`:

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

Use the commit message style recorded in `config.md`:

**Conventional Commits** (default):
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

**Phase-style** (optional):
```text
Phase X.Y: <description>
```
- Uses the roadmap phase label as the commit subject prefix.
- `<description>` is a concise summary of what changed.
- Description defaults to English; use another language only when the user asks.

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

In collaborative mode, this covers private notes and all temporary work, including layout backups. In privacy mode, configuration, the fixed `roadmap/`, and goal archives also live under `.checkpoint-karpathy/private/` and are covered automatically.

Do not add `.checkpoint-karpathy/` wholesale to `.gitignore`, because that would hide roadmap and progress even in collaborative mode.

---

## Final Definition of Done

A subphase is done only when:

- the state directory, commit style, and layout policy match `config.md`,
- its completed roadmap item is checked `[x]` in the active plan, or the plan is explicitly adjusted to reflect the actual outcome,
- code/project files are coherent,
- verification was run or honestly documented as unavailable,
- `.checkpoint-karpathy/roadmap/progress.md` is updated,
- the active plan, current snapshot, and Next Action are updated in the files selected by the layout,
- context and the plan-change log are updated when their information changes,
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
- progress records the final milestone review and overall acceptance evidence,
- Completion is `completed` and the next action is recorded as goal completion.

After full roadmap completion, the skill is no longer active. Do not invoke it again unless the user explicitly asks for checkpoint-karpathy development on a new goal.

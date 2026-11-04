# Project state operations

Read the relevant section before initializing directories, creating configuration, filling missing settings, changing visibility mode, or archiving a goal. Preserve existing state and follow the lifecycle in [SKILL.md](../SKILL.md#completion-and-lifecycle).

## Configuration and initialization

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
```

The state directory is `.checkpoint-karpathy/` in collaborative mode and `.checkpoint-karpathy/private/` in privacy mode. `config.md` sits directly in that directory, alongside the fixed `roadmap/` directory.

During initialization, create the selected state directory and its `roadmap/`, plus `.checkpoint-karpathy/private/work/` in both modes. Reuse existing directories and ensure `.checkpoint-karpathy/private/` is ignored by Git. Create work categories and `archive/` only as needed. An empty `roadmap/` is a directory ready for planning, not an existing goal.

When the user requests settings changes, update only the requested values and apply them to subsequent work. Update uncompleted commit targets for a commit-style change.

For a visibility-mode change, create or reuse the destination `roadmap/`, move the active goal contents into it, and move `config.md` into its parent state directory, preserving content and relative links. Check destination conflicts before moving; do not overwrite state. Keep the source `roadmap/` directory in place. Apply the selected Git tracking policy; include removal of formerly tracked active state paths in the next relevant commit when switching to privacy. Existing Git history remains. Archived goals, other private notes, and `private/work/` retain their locations and visibility.

Paths in these references illustrate collaborative mode. Resolve `config.md`, `roadmap/`, and `archive/` relative to the selected state directory. The work directory always uses `.checkpoint-karpathy/private/work/`.

## Directories and visibility

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

**Roadmap documents:**

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

Use `.checkpoint-karpathy/private/work/` for temporary project files. Create it during initialization in both modes. It stays in place during mode changes and goal archiving. Do not automatically archive or clear its contents when starting a new goal.

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

## Recovering partial state

An empty fixed `roadmap/` is not an existing goal. If goal documents are partial or outside the active directory, preserve and organize them without overwriting or assuming a new goal. Recover missing state from the plan and evidence. Clarify conflicting goals or terminal states with the user.

## Archiving

Archive only when the user invokes the skill for a new goal after the old goal is completed or cancelled. Verify a completed claim against the plan, review commits, and overall acceptance first; cancelled work need not pass unfinished acceptance.

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

The archive has no extra enclosing `roadmap/` layer. Keep `config.md` active and reuse it; leave `private/work/` and its contents in place. Archive on the next invocation for a new goal, not immediately upon completion or cancellation.

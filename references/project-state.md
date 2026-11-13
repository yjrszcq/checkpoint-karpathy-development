# Project state operations

Read the relevant section before initializing directories, creating configuration, filling missing settings, changing visibility mode, or archiving a goal. Preserve existing state and follow the lifecycle in [SKILL.md](../SKILL.md#completion-and-lifecycle).

## Configuration and initialization

Before each use, look for `config.yaml` in `.checkpoint-karpathy/` and `.checkpoint-karpathy/private/`.

- Read an existing configuration and use its settings across conversations and goals. Change settings only at the user's request.
- Create it only if missing, before planning. Use each user-specified setting and the default for anything unspecified.
- If both locations contain a configuration, resolve which is active with the user before proceeding.
- Preserve existing planning content when initializing configuration or filling missing settings. Retain recorded values and add only missing settings with their descriptions and defaults.

Generate a configuration that explains every setting, its accepted values, effects, and default. Use the user's language for the explanations. Users edit the YAML values; comments explain each setting:

```yaml
# Planning visibility and location. Default: collaborative.
# collaborative: Track configuration, project memory, roadmap documents, and archives in Git.
# privacy: Keep them under Git-ignored private/.
mode: collaborative

# Commit subject format. Default: conventional.
# conventional: Conventional Commits, e.g. feat(auth): add login.
# phase: Phase-style, e.g. Phase 1.1: add login.
commit_message_style: conventional
```

The state directory is `.checkpoint-karpathy/` in collaborative mode and `.checkpoint-karpathy/private/` in privacy mode. `config.yaml` sits directly in that directory, alongside `memory.md` and the fixed `roadmap/` directory.

During initialization, create the selected state directory and its `roadmap/` and `memory.md`, plus `.checkpoint-karpathy/private/work/` in both modes. Reuse existing directories and ensure `.checkpoint-karpathy/private/` is ignored by Git. Create work categories and `archive/` only as needed.

When the user requests settings changes, update only the requested values and apply them to subsequent work. Update uncompleted commit targets for a commit-style change.

### Project memory

Initialize `memory.md` together with configuration and fixed directories, using [assets/memory/](../assets/memory/) in the selected language. It starts with three empty categories: User Preferences, Project Conventions, and Lessons Learned. Preserve existing memory byte-for-byte, including on repeated initialization with a different language; backfill only when absent. Resolve symlinks and non-file paths before initialization.

Read memory before planning or resuming each goal. Maintain concise, reusable user preferences, confirmed project conventions, and lessons with their trigger, cause or uncertainty, solution, scope, and useful evidence. Identify the source of a preference or fact when useful; memory cannot override current user instructions or project rules. Mark uncertainty, update stale entries, and avoid duplicating current goal context, status, or execution history. Update only when durable information changes. Keep sensitive details in private notes in either mode.

Creation, completion, cancellation, and archiving preserve memory. It is not one of the six goal documents and is not part of structured goal input. During a visibility change, move it with configuration after checking all destination conflicts. Reconcile existing destination memory instead of overwriting either copy. Collaborative mode tracks memory; privacy mode keeps it ignored.

### Helper commands

Use the installed skill's initialization, goal-creation, and archive scripts. They require Python 3.9+ and PyYAML; if needed, install `scripts/requirements.txt` in the Python environment used to run them. Replace `/path/to/skill` with the installed package directory. `--project` is the actual project root and defaults to the current directory.

For first use, resolve the mode from the user's request or the default and pass it explicitly:

```bash
python3 /path/to/skill/scripts/init_project.py --project /path/to/project --mode collaborative --language en
```

Use `--mode privacy` when requested. `--commit-message-style phase` selects phase subjects on first creation; the default is `conventional`. `--language en|zh` selects configuration comments from [assets/config/](../assets/config/) and the memory template from [assets/memory/](../assets/memory/) (default `en`); use `zh` for Chinese. Translate comments into another user language when appropriate, keeping keys and values intact.

Initialization creates missing `config.yaml` and `memory.md`, the fixed empty `roadmap/`, and `private/work/`, and adds the private ignore rule without replacing `.gitignore`. It preserves existing configuration, memory, and complete goal documents byte-for-byte. On resume, pass the recorded mode; a different mode or commit style is rejected. Recover partial or opposite-mode goal state first.

Before creating a goal, read [Structured goal input](goal-input.md). The agent plans the entire goal and sends structured JSON through standard input to `create_goal.py`. The script validates fields and references and fills the bundled templates.

Use the complete JSON and invocation example in the linked reference. All six documents are rendered before activation. The script sets completion to `incomplete`, generates unchecked subphases and standalone reviews, and writes an initial progress entry for **roadmap generation** and a changelog entry establishing the initial plan. After creation, update documents directly as work progresses; creation refuses any nonempty active roadmap.

When starting a new goal after a completed or cancelled goal, first prepare the complete new JSON and run the creation command with `--check-only`. This validates input and template rendering without writing files or requiring an empty active roadmap. Keep the same validated payload for the creation step. The agent must also verify actual completion evidence or explicit user cancellation before archiving.

```bash
python3 /path/to/skill/scripts/archive_goal.py --project /path/to/project --title linked-market-information
```

The title describes the old goal and contains letters or numbers separated by hyphens. The archive command reads `config.yaml`, determines paths, and supplies the date and collision suffix. It moves all goal contents into the archive and leaves the fixed `roadmap/` empty. Configuration, memory, and work remain active. Then run `create_goal.py` with the validated new content. If creation fails, the old goal is safe in its archive; inspect the reported state before retrying. Explicitly requested archive-only work needs no replacement goal.

The archive script reads `completed` or `cancelled` from the first nonblank line of the `## Completion` section in `status.md`. The agent verifies termination evidence before invoking it. Keep this heading and value intact when translating documents. Reconcile unclear status from evidence before retrying.

The scripts reject conflicting configurations, mismatched mode/location, and overwrites. Initialization and archiving also reject partial goal sets. Creation validates all content and templates before writing, stages rendered documents under `private/work/staging/`, and attempts to return activated files to staging on failure. Archiving attempts to restore the old goal if a move fails. Failed recovery reports the actual paths; preserve partial files and evidence until recovery. Neither command offers crash-proof multi-file transactions; inspect state after process or system termination. The commands do not commit, push, change existing settings, or clean work files. For a user-requested configuration change, edit the YAML values and follow the visibility operations below.

For a visibility-mode change, create or reuse the destination `roadmap/`, move the active goal contents into it, and move `config.yaml` and `memory.md` into its parent state directory, preserving content and relative links. Check all destination conflicts before moving; reconcile competing memory copies without overwriting state. Keep the source `roadmap/` directory in place. Apply the selected Git tracking policy; include removal of formerly tracked active state paths in the next relevant commit when switching to privacy. Existing Git history remains. Archived goals, other private notes, and `private/work/` retain their locations and visibility.

Paths in these references illustrate collaborative mode. Resolve `config.yaml`, `memory.md`, `roadmap/`, and `archive/` relative to the selected state directory. The work directory always uses `.checkpoint-karpathy/private/work/`.

## Directories and visibility

**Collaborative mode:**

```text
.checkpoint-karpathy/
  config.yaml
  memory.md
  roadmap/
  private/
    work/
  archive/
```

**Privacy mode:**

```text
.checkpoint-karpathy/
  private/
    config.yaml
    memory.md
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

In collaborative mode, commit configuration, memory, roadmap contents, and goal archives; ignore `.checkpoint-karpathy/private/`. In privacy mode, keep all state under `private/` untracked. Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential strategy into committed planning documents. Sensitive local notes belong under `private/` in either mode.

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

Create goal documents in an empty `roadmap/`. If documents are partial or outside the active directory, preserve and organize them before proceeding. Recover missing state from the plan and evidence. Clarify conflicting goals or terminal states with the user.

## Archiving

Archive when the user invokes the skill for a new goal after the old goal is completed or cancelled, or explicitly requests archiving a terminal goal without a replacement. Verify a completed claim against the plan, review commits, and overall acceptance first; cancelled work need not pass unfinished acceptance.

Use `archive/YYYYMMDDa-<summary>/` within the selected state directory. The letter increments (`a` … `z`, `aa`, `ab`, …) to avoid same-day collisions. Read the summary from the old goal and use a short kebab-case name describing that completed or cancelled goal.

Create an unused archive destination, then move **all contents** of the active `roadmap/`, including any added subdirectories, directly into it. Check conflicts and preserve relative links within the goal documents. Keep the fixed `roadmap/` directory itself. For a new goal, validate the structured content first, archive, then run the separate creation command.

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

Keep `config.yaml` and `memory.md` active and reuse them; leave `private/work/` and its contents in place.

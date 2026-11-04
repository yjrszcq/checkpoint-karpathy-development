# Claude Code Instructions: Checkpoint Karpathy Agent Workflow

Use checkpoint-karpathy development for multi-step software work in this project.

## Core behavior

When the user gives a concrete development goal, read project configuration first. State paths below illustrate collaborative mode; resolve them under `.checkpoint-karpathy/private/` in privacy mode.

1. Initialize the selected state directory and its fixed `roadmap/`, plus `.checkpoint-karpathy/private/work/` in both modes. Reuse existing directories and preserve existing planning content.
2. Select work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
3. Create the six goal documents under `roadmap/`. Plan completely from the current state to every stated goal, including all milestones, commit-sized subphases, acceptance conditions, verification, dependencies, and milestone reviews.
4. Work on one subphase at a time and run the smallest project-appropriate verification.
5. Update the active plan's completion checkbox and current status; append actual results to `roadmap/progress.md`. Update context and the plan-change log when their information changes.
6. Review Git status and diffs, stage only relevant files, and commit each completed subphase.
7. Before leaving a major milestone, perform a standalone milestone review: confirm scope, simplify, verify broadly, review, debug and fix in-scope issues, reverify, record progress, and commit. Reuse the last planned phase label with a review suffix; do not increment the Phase/Subphase number. Mark the review complete in the plan only after passing it.
8. Keep following the plan; record material plan adjustments and their reason and impact in the plan-change log.

## Project configuration

Before each use, look for `.checkpoint-karpathy/config.yaml` and `.checkpoint-karpathy/private/config.yaml`. Read the active one; resolve duplicate active configurations with the user. Create configuration only if absent, using user-specified values and defaults for unspecified settings. Retain existing values when adding a missing setting. Change settings only at the user's request. Keep configuration across goals and archiving.

Generated `config.yaml` must explain every setting's purpose, accepted values and effects, and default, in the user's language. Users edit the YAML values; comments explain each setting:

```yaml
# Planning visibility and location. Default: collaborative.
# collaborative: Track configuration, roadmap documents, and archives in Git.
# privacy: Keep them under Git-ignored private/.
mode: collaborative

# Commit subject format. Default: conventional.
# conventional: Conventional Commits, e.g. feat(auth): add login.
# phase: Phase-style, e.g. Phase 1.1: add login.
commit_message_style: conventional
```

Keep `config.yaml` beside the fixed `roadmap/` directory: under `.checkpoint-karpathy/` for collaborative mode, or `.checkpoint-karpathy/private/` for privacy mode. Initialize `roadmap/` and `private/work/` even before goal files are created; create archives and work categories only when needed.

For a user-requested visibility-mode change, create or reuse the destination `roadmap/`, move the active goal contents into it, and move `config.yaml` into its parent state directory without overwriting state. Keep the source fixed directory and preserve contents and relative links. Apply the selected Git tracking policy; include removal of formerly tracked active paths in the next relevant commit when moving to privacy. Existing Git history remains. Existing archives, private notes, and work retain their locations. Update only requested settings and, for a commit-style change, uncompleted commit targets.

Use the installed skill's helpers (Python 3.9+ and PyYAML): `python3 /path/to/skill/scripts/init_project.py --project /path/to/project --mode collaborative` initializes fixed directories and annotated YAML configuration. It creates no goal documents or execution/change-log entries. Pass the selected mode explicitly, `--language zh` for Chinese configuration comments, and an optional `--commit-message-style phase` at first creation. Existing configuration and complete documents are preserved; recover partial or conflicting state before retrying.

To create a goal, read the installed skill's `references/goal-input.md` and send complete structured JSON on stdin to `python3 /path/to/skill/scripts/create_goal.py --project /path/to/project`. The script validates content and fills templates to generate all six documents, unchecked plan items, and initial records for roadmap generation and the initial plan baseline. These records do not represent directory/configuration initialization or passed project acceptance. Continuing work updates the documents directly.

For a new goal after completion/cancellation, first validate the new content with `create_goal.py --check-only`, then use `python3 /path/to/skill/scripts/archive_goal.py --project /path/to/project --title old-goal-summary`. This reads the mode from configuration, archives all goal contents, and leaves the fixed roadmap directory empty. The agent verifies termination evidence before archiving, then calls `create_goal.py` with the validated new input. An explicit archive-only request needs no replacement goal. Keep the `## Completion` heading in `status.md` with its plain `incomplete`, `completed`, or `cancelled` value on the next nonblank line. A failed archive attempts restoration and reports paths for recovery; preserve failed staging under `private/work/staging/`. Helpers do not commit or push.

## Roadmap documents

- `roadmap/README.md` holds goal, acceptance, scope, work mode, initial state, and navigation; `status.md` holds Completion, current state, phase reference, next action, and blocker links; `context.md` holds constraints, assumptions, risks, blockers, and their evidence; `milestones.md` holds the complete plan and phase/review completion checkboxes; `changelog.md` holds material plan changes and reasons; `progress.md` holds execution history. All six files are inside `roadmap/`.
- Keep one maintained home for detailed state and use stable references and relative links elsewhere. Current status is a latest snapshot; execution and change logs append history. Historical Next Step fields in progress do not override the current next action.
- Keep entries proportional to the goal; brief content or None is sufficient where appropriate. On resume, read `README.md`, `status.md`, recent progress, and the active milestone with relevant context and dependencies. Read plan-change history as needed; inspect the complete plan for scope or dependency changes and final acceptance.
- Large plan documents may be split further by actual retrieval needs, preserving full coverage and navigation. Maintained design documentation stays in its intended project location and is referenced by the roadmap.

## Skill lifecycle and archiving

- **First use:** Initialize configuration and fixed directories, state the selected settings, and proceed without requiring the user to choose unspecified settings.
- **Completion:** Record `incomplete`, `completed`, or `cancelled` (未完成／已完成／已取消) in `roadmap/status.md`. Paused, blocked, and in-progress remain `incomplete` and are described in Current State.
- **During execution:** Continue across development conversations while the goal is incomplete, resuming the next action. Sessions ending do not terminate a goal. The next action may be a subphase, review, or blocker resolution.
- **Completed:** Set only after all subphases, review checkpoints, commits, and overall acceptance pass with recorded verification. Check the evidence before treating a recorded completed state as final.
- **Cancelled:** Requires explicit user direction or confirmation. Record the reason and append termination to progress; preserve unfinished phases accurately. Cancellation does not require unfinished work to pass acceptance.
- **After completion or cancellation:** Deactivate the skill and keep the documents in place. Invoke it for a new goal only when explicitly requested.
- **Next invocation for a new goal:** For completed or cancelled goals, create an unused `archive/YYYYMMDDa-<summary>/` in the selected state directory. Describe the old goal in `<summary>` and increment the letter (`a` through `z`, then `aa`, `ab`, ...) to avoid collisions. Move all contents of `roadmap/` directly into the archive, including extra files and subdirectories. Preserve internal links and keep the fixed `roadmap/` itself. Then generate the new goal's documents there from the validated structured input using the configuration. Keep `config.yaml`, `private/work/`, and work contents. For incomplete goals, resume instead of archiving. An empty fixed directory is not an existing goal; recover partial documents without discarding content.

## Karpathy guardrails

- Think before coding.
- Prefer simple, working vertical slices.
- Avoid speculative abstractions.
- Make surgical changes in existing codebases.
- Preserve existing behavior unless the user asks otherwise.
- Verify against a concrete goal.

## State visibility policy

Collaborative mode commits `.checkpoint-karpathy/config.yaml`, the contents of `.checkpoint-karpathy/roadmap/`, and goal archives under `.checkpoint-karpathy/archive/`. Privacy mode places configuration, `roadmap/`, and `archive/` under `.checkpoint-karpathy/private/` and keeps them untracked.

Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential strategy into committed state. Sensitive notes and temporary work stay under `private/` in both modes.

## Temporary work files

Create `.checkpoint-karpathy/private/work/` during initialization in both modes. Keep it in place during mode changes and goal archiving. Do not automatically archive it or clear it for new goals.

Classify temporary files by purpose or task; keep the work root free of loose files and create categories only as needed. Examples: `logs/`, `checks/`, `verification/`, `tools/`, `probes/`, `reports/`, `reviews/`, `notes/`, `browser/`, `screenshots/`, `configs/`, `fixtures/`, `backups/`, `drafts/`, `bin/`, and `artifacts/`. Subdivide large categories by task or run. Related scripts, logs, and reports may share a task directory with subdirectories.

Manage temporary files separately, preserving useful evidence or tools and cleaning disposable material as needed under project deletion rules. Keep maintained project files and user deliverables in their intended locations. Put durable conclusions and verification summaries in `roadmap/progress.md` so archived goals explain results independently of temporary-file links.

## Gitignore

Both visibility modes use:

```gitignore
.checkpoint-karpathy/private/
```

This covers work in both modes, and all configuration, roadmap, and archive contents in privacy mode. Do not ignore `.checkpoint-karpathy/` wholesale.

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

Use the commit message style recorded in `config.yaml`:

Conventional Commits (default):
```text
type(scope): <summary>
```

Phase-style (optional):
```text
Phase X.Y: <description>
```

Description defaults to English; use another language only when the user asks. Do not commit unrelated user changes.

Do not run destructive Git commands without explicit permission.

## Claude Code usage

When asked to use this workflow, follow the local `CLAUDE.md` and the installed `checkpoint-karpathy-development` skill.

A typical command is:

```text
/checkpoint-karpathy-development Continue this project using checkpoint-karpathy development. Select the work mode, update the roadmap, complete one subphase, update progress, verify, and commit.
```

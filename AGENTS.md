# Checkpoint Karpathy Agent Workflow

Use checkpoint-karpathy development for multi-step software work in this project.

## Core behavior

When the user gives a concrete development goal, read project configuration first. State paths below illustrate collaborative mode; resolve them under `.checkpoint-karpathy/private/` in privacy mode.

1. Initialize the selected state directory and its fixed `roadmap/`, plus `.checkpoint-karpathy/private/work/` in both modes. Reuse existing directories and preserve existing planning content.
2. Select work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
3. Select the goal's document layout according to configuration. Plan completely from the current state to every stated goal, including all milestones, commit-sized subphases, acceptance conditions, verification, dependencies, and milestone reviews.
4. Work on one subphase at a time and run the smallest project-appropriate verification.
5. Update the active plan's completion checkbox and current status; append actual results to `roadmap/progress.md`. Update context and the plan-change log when their information changes.
6. Review Git status and diffs, stage only relevant files, and commit each completed subphase.
7. Before leaving a major milestone, perform a standalone milestone review: confirm scope, simplify, verify broadly, review, debug and fix in-scope issues, reverify, record progress, and commit. Reuse the last planned phase label with a review suffix; do not increment the Phase/Subphase number. Mark the review complete in the plan only after passing it.
8. Keep following the plan; record material plan adjustments and their reason and impact in the plan-change log.

## Project configuration

Before each use, look for `.checkpoint-karpathy/config.md` and `.checkpoint-karpathy/private/config.md`. Read the active one; resolve duplicate active configurations with the user. Create configuration only if absent, using user-specified values and defaults for unspecified settings. Retain existing values when adding a missing setting. Change settings only at the user's request. Keep configuration across goals and archiving.

Generated `config.md` must explain every setting's purpose, accepted values and effects, and default, in the user's language. Users edit the `Value` for each setting:

```md
# Checkpoint Karpathy Configuration

## Mode
- Value: collaborative
- Purpose: Select planning visibility and location.
- Accepted values:
  - collaborative: Track configuration, roadmap documents, and goal archives in Git.
  - privacy: Keep configuration, roadmap documents, and goal archives under Git-ignored private/.
- Default: collaborative

## Commit message style
- Value: conventional
- Purpose: Select commit subject format.
- Accepted values:
  - conventional: Conventional Commits, such as feat(auth): add login.
  - phase: Phase-style, such as Phase 1.1: add login.
- Default: conventional

## Roadmap layout
- Value: auto
- Purpose: Select document organization for the entire goal.
- Accepted values:
  - auto: Let the agent assess and switch between compact and structured layouts.
  - compact: Use roadmap/roadmap.md and roadmap/progress.md; switch only at the user's request.
  - structured: Separate overview, status, context, milestones, changelog, and progress under roadmap/; switch only at the user's request.
- Default: auto
```

Keep `config.md` beside the fixed `roadmap/` directory: under `.checkpoint-karpathy/` for collaborative mode, or `.checkpoint-karpathy/private/` for privacy mode. Initialize `roadmap/` and `private/work/` even before goal files are created; create archives and work categories only when needed.

For a user-requested visibility-mode change, create or reuse the destination `roadmap/`, move the active goal contents into it, and move `config.md` into its parent state directory without overwriting state. Keep the source fixed directory and preserve contents and relative links. Apply the selected Git tracking policy; include removal of formerly tracked active paths in the next relevant commit when moving to privacy. Existing Git history remains. Existing archives, private notes, and work retain their locations. Update only requested settings and, for a commit-style change, uncompleted commit targets.

## Layout and document responsibilities

- **Compact:** `roadmap/roadmap.md` holds goal, overall acceptance, scope, work mode, initial state, Completion, current state, next action, constraints, assumptions, risks and blockers, the full milestone plan, and a Roadmap Change Log. `roadmap/progress.md` holds actual execution history. No separate README is needed.
- **Structured:** `roadmap/README.md` holds goal, acceptance, scope, work mode, initial state, and navigation; `status.md` holds Completion, current state, phase reference, next action, and blocker links; `context.md` holds constraints, assumptions, risks, blockers, and their evidence; `milestones.md` holds the complete plan and phase/review completion checkboxes; `changelog.md` holds material plan changes and reasons; `progress.md` holds execution history. All six files are inside `roadmap/`.
- Keep one maintained home for detailed state and use stable references and relative links elsewhere. Current status is a latest snapshot; execution and change logs append history. Historical Next Step fields in progress do not override the current next action.
- With `auto`, assess the whole goal's plan, dependencies, background, design evolution, and accumulated history. Choose and reassess either layout; do not decide from remaining task count or switch repeatedly with little benefit. Keep configuration as `auto`. With a fixed layout, switch only on user request.
- Before switching, copy all current goal contents into a unique `.checkpoint-karpathy/private/work/backups/roadmap-layout/<timestamp>-<source>-to-<target>/` and verify the backup. Interpret documents by meaning even when headings differ from templates. Preserve all content, IDs, state, acceptance, and history; check conflicts, update links, and verify the result against the backup. Move superseded files individually to a separate backup subdirectory. Preserve failed output separately and restore the original contents if the switch fails. Record the reason, layouts, and backup path in the active plan-change log. Switching does not archive a goal.
- Large plan documents may be split further by actual retrieval needs, preserving full coverage and navigation. Maintained design documentation stays in its intended project location and is referenced by the roadmap.

## Skill lifecycle and archiving

- **First use:** Initialize configuration and fixed directories, state the selected settings, and proceed without requiring the user to choose unspecified settings.
- **Completion:** Record `incomplete`, `completed`, or `cancelled` (未完成／已完成／已取消) in the compact roadmap or structured status. Paused, blocked, and in-progress remain `incomplete` and are described in Current State.
- **During execution:** Continue across development conversations while the goal is incomplete, resuming the next action. Sessions ending do not terminate a goal. The next action may be a subphase, review, or blocker resolution.
- **Completed:** Set only after all subphases, review checkpoints, commits, and overall acceptance pass with recorded verification. Check the evidence before treating a recorded completed state as final.
- **Cancelled:** Requires explicit user direction or confirmation. Record the reason and append termination to progress; preserve unfinished phases accurately. Cancellation does not require unfinished work to pass acceptance.
- **After completion or cancellation:** Deactivate the skill and keep the documents in place. Invoke it for a new goal only when explicitly requested.
- **Next invocation for a new goal:** For completed or cancelled goals, create an unused `archive/YYYYMMDDa-<summary>/` in the selected state directory. Describe the old goal in `<summary>` and increment the letter (`a` through `z`, then `aa`, `ab`, ...) to avoid collisions. Move all contents of `roadmap/` directly into the archive, including extra files and subdirectories, without an enclosing `roadmap/` layer. Preserve internal links and keep the fixed `roadmap/` itself. Then initialize the new goal's documents there using the configuration. Keep `config.md`, `private/work/`, and work contents. For incomplete goals, resume instead of archiving. An empty fixed directory is not an existing goal; recover partial documents without discarding content.

## Karpathy guardrails

- Think before coding.
- Prefer simple, working vertical slices.
- Avoid speculative abstractions.
- Make surgical changes in existing codebases.
- Preserve existing behavior unless the user asks otherwise.
- Verify against a concrete goal.

## State visibility policy

Collaborative mode commits `.checkpoint-karpathy/config.md`, the contents of `.checkpoint-karpathy/roadmap/`, and goal archives under `.checkpoint-karpathy/archive/`. Privacy mode places configuration, `roadmap/`, and `archive/` under `.checkpoint-karpathy/private/` and keeps them untracked.

Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential strategy into committed state. Sensitive notes and temporary work stay under `private/` in both modes.

## Temporary work files

Create `.checkpoint-karpathy/private/work/` during initialization in both modes. Keep it in place during mode and layout changes and goal archiving. Do not automatically archive it or clear it for new goals.

Classify temporary files by purpose or task; keep the work root free of loose files and create categories only as needed. Examples: `logs/`, `checks/`, `verification/`, `tools/`, `probes/`, `reports/`, `reviews/`, `notes/`, `browser/`, `screenshots/`, `configs/`, `fixtures/`, `backups/`, `drafts/`, `bin/`, and `artifacts/`. Subdivide large categories by task or run. Related scripts, logs, and reports may share a task directory with subdirectories.

Manage temporary files separately, preserving useful evidence or tools and cleaning disposable material as needed under project deletion rules. Keep maintained project files and user deliverables in their intended locations. Put durable conclusions and verification summaries in `roadmap/progress.md` so archived goals explain results independently of temporary-file links.

## Gitignore

Both visibility modes use:

```gitignore
.checkpoint-karpathy/private/
```

This covers work and layout backups in both modes, and all configuration, roadmap, and archive contents in privacy mode. Do not ignore `.checkpoint-karpathy/` wholesale.

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

Use the commit message style recorded in `config.md`:

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

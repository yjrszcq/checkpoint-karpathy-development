---
name: checkpoint-karpathy-development
license: MIT
description: "Use this skill for roadmap-driven, checkpointed software work across greenfield development, continuation, feature work, bug fixing, refactoring, and maintenance, while following Karpathy-inspired engineering guardrails."
---

# Checkpoint Karpathy Development

Plan the full goal, execute commit-sized subphases, record evidence, and resume reliably across session or context loss. Each major milestone ends with a separate review checkpoint.

This workflow supports greenfield development, continuation, features, bug fixes, refactoring, maintenance, release preparation, and development-related documentation or configuration work.

## Engineering guardrails

- Before meaningful edits, identify the goal, work mode, smallest coherent subphase, assumptions, risks, and verification. For ambiguous or high-risk work, briefly state the plan; proceed directly for clear, low-risk work.
- Prefer the simplest working vertical slice. Avoid speculative abstractions, unused frameworks, unnecessary layers, broad rewrites, and premature generalization.
- In existing projects, preserve behavior unless the user requests a change; match local style, touch relevant files only, and avoid unrelated refactors. In greenfield work, build the minimum runnable or inspectable structure needed for the current subphase.
- Give each subphase a concrete goal, completion condition, verification method, and commit. Verify against observable results.

## Configuration and fixed paths

Before every use, look for `config.yaml` in `.checkpoint-karpathy/` and `.checkpoint-karpathy/private/`. Read the active configuration first. If both exist, resolve the active one with the user before proceeding.

| Setting | Values | Default |
|---|---|---|
| `mode` | `collaborative`, `privacy` | `collaborative` |
| `commit_message_style` | `conventional`, `phase` | `conventional` |

Create configuration only if missing, using user choices and defaults for unspecified settings. Explain every setting's purpose, accepted values and effects, and default in the user's language. Retain existing values when filling missing settings. Keep configuration across goals and archives; change settings only at the user's request. On first use, briefly state the recorded choices and proceed without asking the user to choose unspecified values.

The state directory is `.checkpoint-karpathy/` in collaborative mode or `.checkpoint-karpathy/private/` in privacy mode. Paths below are relative to it; paths beginning with `.checkpoint-karpathy/` are relative to the project root:

- `config.yaml`: persistent project configuration.
- `roadmap/`: fixed directory containing the active goal documents.
- `archive/`: completed or cancelled goal contents, created as needed.

Use the bundled [initialization command](scripts/init_project.py) to create configuration, the fixed empty `roadmap/`, and `.checkpoint-karpathy/private/work/` in both modes. Pass the selected mode explicitly; use defaults for unspecified settings. Send agent-prepared structured JSON on standard input to the [creation command](scripts/create_goal.py); it fills templates with actual content, creates all six goal documents with unchecked plan items, and records roadmap generation and the initial plan baseline. Read [Structured goal input](references/goal-input.md) before preparing content. The [archive command](scripts/archive_goal.py) reads configuration and moves a terminal goal's contents into its archive, leaving the fixed roadmap directory empty. Commands, dependencies, and recovery are in [Project state operations](references/project-state.md#helper-commands).

Before initializing directories, creating configuration, filling missing settings, or changing visibility mode, read [Project state operations](references/project-state.md#configuration-and-initialization). It defines the annotated configuration and directory operations. For archiving, read its [Archiving procedure](references/project-state.md#archiving) before moving files.

On requested settings changes, apply only the requested values to subsequent work. Update uncompleted commit targets for a commit-style change. During visibility-mode changes, move active goal contents into the destination `roadmap/` and configuration into its parent state directory without overwriting state. Keep fixed directories, archives, private notes, and work in place as specified by the project-state procedure.

## Start or resume

1. Read project instructions and configuration, initialize missing fixed directories, and inspect the actual goal files.
2. Read `roadmap/README.md` and `roadmap/status.md`, then recent progress and the active milestone, dependencies, and relevant context or blockers. Read plan-change history when needed to understand a decision.
3. If goal files are absent, plan the full goal and create its documents using structured input. For partial or misplaced documents, read [Recovering partial state](references/project-state.md#recovering-partial-state); preserve content and recover from evidence. Clarify conflicting goals or terminal states with the user.
4. If Completion is `incomplete`, resume the next unfinished action: a subphase, milestone review, or blocker resolution. Check the complete plan before changing scope or cross-milestone dependencies.
5. If `completed`, verify the claim against plan checkboxes, review commits, and overall acceptance evidence; reconcile inconsistencies before archiving.
6. If `completed` or `cancelled` and starting an explicitly requested new goal, prepare and validate the new goal input with `create_goal.py --check-only`, archive the old goal, then run `create_goal.py` with the validated input inside the same `roadmap/`. Retain configuration and work.

Select and record the work mode in `roadmap/README.md`:

- `greenfield`: empty or near-empty repository.
- `continuation`: ongoing work in an existing codebase.
- `feature`: add a capability.
- `bugfix`: reproduce, isolate, fix, and verify a defect.
- `refactor`: change structure while preserving behavior.
- `maintenance`: careful work near release or in a mature project.

## Roadmap documents

Plan completely from the current repository state to every stated goal. Include all milestones, dependencies, commit-sized subphases, scope, success criteria, verification, commit targets, a standalone review for each milestone, overall acceptance, and the next action.

Read [Roadmap templates](references/roadmap-templates.md) before creating or reorganizing goal documents. Choose milestones to cover the complete goal. Interpret existing documents by meaning even when headings differ.

All active goal documents live inside the fixed `roadmap/`:

| Document | Information |
|---|---|
| `README.md` | Goal, overall acceptance, scope, work mode, initial state, navigation |
| `status.md` | Completion, current snapshot, current phase reference, Next Action |
| `context.md` | Constraints, assumptions, risks, blockers, states and evidence |
| `milestones.md` | Full plan, dependencies, criteria, verification, commit targets, subphase and review checkboxes |
| `changelog.md` | Material plan-change reasons, changes, affected phases and impact |
| `progress.md` | Actual work, verification, commits, execution decisions and issue handling |

Create all six files. Keep content proportional to the goal; brief entries or an explicit None suffice where there is little to record. Each detailed item has one maintained home; use stable identifiers and relative links elsewhere. Keep the authoritative current snapshot and Next Action in status; append execution and plan-change histories.

Read the sections needed for the current action. Review the complete plan when initially planning, changing scope or dependencies across milestones, or checking full-goal completion. Update documents only when their information changes; routine checkpoints update milestone checkboxes, status, and progress together.

Update the plan when requirements, priorities, assumptions, blockers, repository evidence, or phase organization change materially. Record why and what changed and its impact in the plan-change log; link execution entries to it. Routine checkboxes and next-action updates need no change entry.

For large documents, split further by actual retrieval needs, preserving navigation, full coverage, identifiers, and histories. Added files and subdirectories belong to the goal for archiving. Keep maintained design documentation in its project location and reference it; record scheduling effects of design changes in the plan-change log.

## Checkpoint execution

Execute one coherent subphase or milestone review at a time:

1. Select the next action and briefly state its goal. Inspect the affected project files and instructions.
2. Make the smallest coherent change that meets the planned scope and success criteria.
3. Detect the project stack and run the smallest relevant verification. Follow Verification and Git below.
4. Check off completed roadmap items: change `[ ]` to `[x]` in `roadmap/milestones.md` and any split milestone documents once completion and verification requirements are met. Leave unfinished, blocked, and cancelled items unchecked.
5. Append the actual work, files changed, verification results, decisions, known issues, and next step to `roadmap/progress.md`. Before creating or reconstructing this log, read the [Progress template](references/checkpoint-details.md#progress-template). Preserve useful prior history.
6. Update the current snapshot, phase reference, and Next Action in `roadmap/status.md`. Update context and the plan-change log when their information changes. If all subphases of a milestone are done, the next action is its standalone review.
7. Review status and diffs, stage relevant files, inspect the staged diff, and commit the checkpoint with its plan checkboxes, progress, and current state. Report the commit and next action.
8. Continue to the next action until the goal is complete, the conversation ends, or the user pauses or cancels. Resume an incomplete goal across development conversations without requiring re-invocation.

Each subphase checkpoint commit includes coherent project changes, verified plan checkboxes, progress, and current status.

### Milestone review

After all planned subphases in a milestone are complete and committed, perform a standalone review before starting the next milestone or declaring the goal done. Read the [Milestone review procedure](references/checkpoint-details.md#milestone-review) before each review.

Confirm scope, simplify, verify broadly, review for regressions and integration gaps, debug and fix in-scope issues, then reverify. Record the ordered findings and final results in progress. Only then check off the review and make its separate commit using the shared checkpoint steps above.

Reuse the last planned phase label with a review suffix, such as `Phase 1.2 Milestone Review: stabilize authentication`. Use this phase reference with either commit message style.

If a blocking issue cannot be fixed, record it in context and progress, update the plan, and commit only a coherent checkpoint; leave the review unchecked. Scope changes, investigation, urgent fixes, and plan corrections may use a temporary checkpoint for the immediate coherent goal, followed by a return to the roadmap.

For the final review, also verify overall acceptance and record its evidence. Set Completion to `completed` and Next Action to goal completion in the closeout commit only when all planned work and review requirements pass. Completion becomes final when that commit succeeds.

## Completion and lifecycle

Record Completion in `roadmap/status.md`. Keep the machine-readable `## Completion` heading followed by the plain value below on its own line, even when translating other headings:

| Value | Meaning |
|---|---|
| `incomplete` | Goal remains active; resume the next unfinished action. |
| `completed` | All subphases and milestone reviews are done and committed, and overall acceptance has recorded verification evidence. |
| `cancelled` | The user explicitly requests or confirms termination. |

Paused, blocked, and in-progress belong in Current State and remain `incomplete`. Session endings do not terminate a goal. Do not infer cancellation from difficulty, inactivity, or blockers. On cancellation, record the reason in the completion document and append termination to progress; preserve completed work and unfinished checkboxes accurately.

After completion or cancellation, report the outcome, deactivate this workflow, and leave goal documents in place unless the user explicitly requests archiving. Invoke it for a new goal only when explicitly requested. On that next invocation, archive all goal contents directly into `archive/YYYYMMDDa-<old-goal-summary>/`, preserving extra files and subdirectories. Keep the fixed `roadmap/` and reuse configuration and work. Follow [Archiving](references/project-state.md#archiving) before moving files; cancelled work need not pass unfinished acceptance.

## Temporary work and visibility

Use `.checkpoint-karpathy/private/work/` in both modes. Keep its root free of loose files; create meaningful purpose- or task-specific subdirectories only as needed. Subdivide large categories by task or run. See [Temporary work files](references/project-state.md#temporary-work-files) for category examples when deciding where material belongs.

Keep work in place across visibility changes and goal archiving. Do not automatically archive or clear it for a new goal. Retain useful tools and evidence; clean disposable content separately under project deletion rules. Keep maintained source, tests, and deliverables in their intended project locations. Record durable conclusions and verification summaries in progress so archives explain results independently of temporary links; raw evidence can remain in work with its path recorded.

Collaborative mode commits configuration, roadmap contents, and goal archives. Privacy mode keeps them untracked under `private/`; include removal of formerly tracked active paths in the next relevant commit after a privacy switch. Existing Git history remains. Never put secrets, credentials, private customer data, sensitive vulnerability details, or confidential strategy in committed state. Sensitive notes belong under `private/` in either mode.

Both modes require this single Git ignore entry:

```gitignore
.checkpoint-karpathy/private/
```

Do not ignore `.checkpoint-karpathy/` wholesale. The private rule covers work in both modes, plus configuration, roadmap documents, and archives in privacy mode.

## Verification and Git

Inspect project documentation, instructions, manifests, and existing checks before choosing commands. Prefer project-declared commands. Use the smallest relevant test, build, typecheck, lint, compile, smoke check, or manual inspection. For unclear checks, consult [Verification discovery](references/checkpoint-details.md#verification-discovery). Record unavailable verification and its reason; never claim an unrun check passed.

For every checkpoint, perform these steps in order:

1. Run `git status` and `git diff` before staging; inspect relevant changes.
2. Stage only relevant project and state files, preserving privacy policy and unrelated user changes.
3. Run `git diff --staged` and inspect it before committing.
4. Commit with the style in `config.yaml`, using a concise, specific, action-oriented description. Descriptions default to English; use another language only at the user's request.

| Style | Normal checkpoint | Milestone review |
|---|---|---|
| `conventional` (default) | `type(scope): summary` | `type(scope): review summary` |
| `phase` | `Phase X.Y: description` | `Phase X.Y Milestone Review: description` |

Do not commit unrelated user changes. Do not run destructive Git commands without explicit permission, including `git reset --hard`, `git clean`, `git rebase`, `git commit --amend`, `git push --force`, or blanket checkout/restore operations.

If Git is absent and the user requested checkpointed development, initialize it with `git init`. If a commit fails because identity is missing, do not fabricate identity; report the issue and request Git identity configuration.

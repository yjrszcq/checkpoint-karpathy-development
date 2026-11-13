# Roadmap document templates

Use these templates when generating a goal or reorganizing its documents. Match the user's language and project needs. Preserve equivalent content in documents whose headings differ. Plan completely for every milestone and supply its content through the structured creation input.

All paths in this reference are relative to the active `roadmap/`. `config.yaml` and project-level `memory.md` live one level above it; memory is not a goal document and is not archived with the goal.

## Goal documents

The creation script fills templates from [assets/roadmap/](../assets/roadmap/) using [structured goal input](goal-input.md). Supply actual content in the user's language, keeping it proportional to the goal. Empty context arrays render as None. Each detailed item has one maintained home; other documents link to it.

### README.md

Template: [README.md](../assets/roadmap/README.md).

### status.md

Template: [status.md](../assets/roadmap/status.md).

### context.md

Template: [context.md](../assets/roadmap/context.md).

Keep reusable project preferences, conventions, and lessons in `../memory.md`; use this document for goal-specific context. Keep assumptions distinct from confirmed constraints, and risks distinct from current obstacles. Assumption states can be unverified, confirmed, or disproved; link to evidence and affected plan changes. Retain useful context when resolving an item, keeping active entries easy to find; append the handling history to progress.

### milestones.md

Template: [milestones.md](../assets/roadmap/milestones.md).

The script renders every supplied milestone with [milestone.md](../assets/roadmap/milestone.md) and each subphase with [phase.md](../assets/roadmap/phase.md), including a separate unchecked review per milestone. Choose the number of milestones and subphases from the complete goal.

### changelog.md

Template: [changelog.md](../assets/roadmap/changelog.md).

The creation script records the initial plan baseline. Append material plan changes chronologically using the following structure; keep execution history in progress. Routine checkbox and next-action updates need no change entry.

```md
## <YYYY-MM-DD> CH-<next number>: <Adjustment title>
- Reason: <Requirement or evidence that changed the plan.>
- Change: <What changed in the current plan.>
- Affected items: <Stable milestone and subphase IDs, with links.>
- Impact: <Scope, dependencies, acceptance, verification, or priorities.>
- Evidence / related execution: <Links to context, design, or progress.>
```

### progress.md

Template: [progress.md](../assets/roadmap/progress.md). The creation script records roadmap generation as the first entry, including structural validation and the unfinished development scope.

Read the [Progress template](checkpoint-details.md#progress-template) before creating or reconstructing execution records. Append concise execution entries with evidence, remaining scope, and handoff details; preserve useful prior history. Keep the current state snapshot in status.md and plan changes in changelog.md.

## Milestone content

Populate `milestones.md` for every milestone, preserving stable references when inserting or reorganizing work. Add an explicit anchor where needed to preserve an existing link.

The [milestone template](../assets/roadmap/milestone.md) includes a standalone review for every milestone. Supply the actual review verification and commit target with the initial structured content.

The review uses the last planned subphase label. Conventional commit targets use `type(scope): summary`; Phase-style targets use `Phase X.Y: description`, or `Phase X.Y Milestone Review: description` for the review. Subjects default to English.

Change each completed item's `[ ]` to `[x]` as soon as its completion and verification requirements are met, including milestone reviews separately. Update the active plan alongside progress and include both in the checkpoint commit. Unfinished, blocked, and cancelled items remain unchecked.

## Completion and document growth

Completion is `incomplete`, `completed`, or `cancelled`. Verify full-goal acceptance and all committed milestone reviews before setting `completed`. Cancellation is explicit user direction and preserves the actual stage completion state.

Keep the `## Completion` heading and the status value on its own line in `status.md` for the archive command. Other document content can follow the user's language.

Preserve user-added sections and all historical entries when reorganizing documents. Larger plans may use a `milestones/` directory with a navigable index; added files and directories are part of the goal and travel with its contents during archiving.

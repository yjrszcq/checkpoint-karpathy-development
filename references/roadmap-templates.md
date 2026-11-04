# Roadmap document templates

Use these examples when initializing a goal or reorganizing its documents. Match the user's language and project needs. Preserve equivalent content in documents whose headings differ. Fill the complete plan for every milestone, using the linked milestone skeleton as needed.

All paths in this reference are relative to the active `roadmap/`. `config.yaml` lives one level above it. The [progress skeleton](../assets/roadmap/progress.md) starts empty. Read the [Progress template](checkpoint-details.md#progress-template) before creating or reconstructing `progress.md`.

## Goal documents

The scripts copy the six skeletons from [assets/roadmap/](../assets/roadmap/). Fill them in the user's language, keeping entries proportional to the goal. Use brief content or None where appropriate. Each detailed item has one maintained home; other documents link to it.

### README.md

Skeleton: [README.md](../assets/roadmap/README.md).

### status.md

Skeleton: [status.md](../assets/roadmap/status.md).

### context.md

Skeleton: [context.md](../assets/roadmap/context.md).

Keep assumptions distinct from confirmed constraints, and risks distinct from current obstacles. Assumption states can be unverified, confirmed, or disproved; link to evidence and affected plan changes. Retain useful context when resolving an item, keeping active entries easy to find; append the handling history to progress.

### milestones.md

Skeleton: [milestones.md](../assets/roadmap/milestones.md).

### changelog.md

Skeleton: [changelog.md](../assets/roadmap/changelog.md).

Keep plan changes separate from execution history; ordinary checkbox and next-action updates need no change entry.

## Milestone content

Populate `milestones.md` for every milestone, preserving stable references when inserting or reorganizing work. Add an explicit anchor where needed to preserve an existing link.

Use the [milestone skeleton](../assets/roadmap/milestones.md) for every milestone, including its standalone review.

The review uses the last planned subphase label; it does not increment the Phase/Subphase number. Conventional commit targets use `type(scope): summary`; Phase-style targets use `Phase X.Y: description`, or `Phase X.Y Milestone Review: description` for the review. Subjects default to English.

Change each completed item's `[ ]` to `[x]` as soon as its completion and verification requirements are met, including milestone reviews separately. Update the active plan alongside progress and include both in the checkpoint commit. Unfinished, blocked, and cancelled items remain unchecked.

## Completion and document growth

Completion is `incomplete`, `completed`, or `cancelled` (未完成／已完成／已取消). Verify full-goal acceptance and all committed milestone reviews before setting `completed`. Cancellation is explicit user direction and preserves the actual stage completion state.

Keep the `## Completion` heading and the status value on its own line in `status.md` for the archive command. Other document content can follow the user's language.

Preserve user-added sections and all historical entries when reorganizing documents. Larger plans may use a `milestones/` directory with a navigable index; added files and directories are part of the goal and travel with its contents during archiving.

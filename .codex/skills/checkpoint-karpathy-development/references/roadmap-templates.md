# Roadmap document templates

Use these examples when initializing a goal or reorganizing its documents. Match the user's language and project needs. Preserve equivalent content in documents whose headings differ. Fill the complete plan for every milestone, not only the example milestone below.

All paths in this reference are relative to the active `roadmap/`. `config.md` lives one level above it. For either layout, read the [Progress template](checkpoint-details.md#progress-template) before creating or reconstructing `progress.md`.

## Compact layout

Create `roadmap.md` and `progress.md`. `roadmap.md` is the entry point:

```md
# Checkpoint Karpathy Roadmap

## Goal
<Concrete goal.>

## Overall Acceptance Criteria
- <Observable condition for the complete goal, with its verification method.>

## Scope
- Included: <scope>
- Non-goals: <boundaries>

## Work Mode
<greenfield | continuation | feature | bugfix | refactor | maintenance>

## Initial State
<Repository baseline when this goal started.>

## Completion
incomplete
<For cancelled: cancellation reason and progress entry link.>

## Current State
<Latest snapshot; paused or blocked if applicable.>

## Current Phase
<Stable phase or review reference in Major Milestones.>

## Next Action
<Subphase, milestone review, or blocker-resolution action.>

## Constraints
- C-01: <Confirmed requirement or boundary.>

## Assumptions
- A-01: <Claim, rationale, validation method, status, evidence link.>

## Risks / Blockers
- R-01: <Risk, impact, response, current status.>
- B-01: <Active blocker, affected phase, resolution path, evidence link.>

## Major Milestones
<Insert every milestone using the Milestone Content example below.>

## Roadmap Change Log
- <Dated material adjustment with reason, affected phase IDs, impact, and links.>

## Navigation
- [Execution history](progress.md)
```

## Structured layout

Create all six files. Each detailed item has one maintained home; other documents link to it.

### README.md

```md
# Goal Overview

## Goal
<Concrete goal.>

## Overall Acceptance Criteria
- <Observable condition for the complete goal, with its verification method.>

## Scope
- Included: <scope>
- Non-goals: <boundaries>

## Work Mode
<greenfield | continuation | feature | bugfix | refactor | maintenance>

## Initial State
<Repository baseline when this goal started.>

## Navigation
- [Current status and completion](status.md)
- [Constraints, assumptions, risks, and blockers](context.md)
- [Complete milestone plan](milestones.md)
- [Plan-change history](changelog.md)
- [Execution history](progress.md)
```

### status.md

```md
# Goal Status

## Completion
incomplete
<For cancelled: cancellation reason and progress entry link.>

## Current State
<Latest snapshot of what exists and what is missing.>

## Current Phase
<Link to the active milestone, subphase, or review in the plan.>

## Next Action
<Subphase, milestone review, or blocker-resolution action, with a link.>

## Related Blockers
<Links to current blocker entries in context.md, or None.>
```

### context.md

```md
# Goal Context

## Constraints
- C-01: <Confirmed requirement or boundary.>

## Assumptions
- A-01: <Claim, rationale, validation method, status, evidence link.>

## Risks
- R-01: <Potential problem, impact, response, current status.>

## Blockers
- B-01: <Existing obstacle, affected phase, resolution path, current status.>
```

Keep assumptions distinct from confirmed constraints, and risks distinct from current obstacles. Assumption states can be unverified, confirmed, or disproved; link to evidence and affected plan changes. Retain useful context when resolving an item, keeping active entries easy to find; append the handling history to progress.

### milestones.md

```md
# Milestone Plan

<Insert every milestone using the Milestone Content example below.>
```

### changelog.md

```md
# Roadmap Change Log

## <YYYY-MM-DD> CH-01: <Adjustment title>
- Reason: <Requirement or evidence that changed the plan.>
- Change: <What changed in the current plan.>
- Affected items: <Stable milestone and subphase IDs, with links.>
- Impact: <Scope, dependencies, acceptance, verification, or priorities.>
- Evidence / related execution: <Links to context, design, or progress.>
```

Use equivalent entries inside the compact roadmap's Roadmap Change Log. Layout conversions also record source and target layouts and the backup path. Keep plan changes separate from execution history; ordinary checkbox and next-action updates need no change entry.

## Milestone content

Use this content in the compact roadmap's Major Milestones section or in the structured milestone plan. Repeat for every milestone, preserving stable references when inserting or reorganizing work. Add an explicit anchor where needed to preserve an existing link.

```md
## Milestone 1: <Title>
Purpose: <Contribution to the overall goal.>
Dependencies: <Other milestones, constraints, or assumptions; None if independent.>

- [ ] 1.1 <Commit-sized goal>
  - Dependencies: <Prerequisite phase IDs or None.>
  - Scope: <What changes.>
  - Success criteria: <Observable completion condition.>
  - Verification: <Project-appropriate command or inspection.>
  - Commit target: <Subject in the configured commit style.>

- [ ] 1.2 <Commit-sized goal>
  - Dependencies: <Prerequisite phase IDs or None.>
  - Scope: <What changes.>
  - Success criteria: <Observable completion condition.>
  - Verification: <Project-appropriate command or inspection.>
  - Commit target: <Subject in the configured commit style.>

- [ ] Milestone 1 Review
  - Trigger: After every planned subphase above is complete and committed.
  - Phase label: Phase 1.2 Milestone Review: <Summary>
  - Scope: Work introduced or substantially touched by this milestone.
  - Order: Confirm scope, simplify, verify broadly, review, debug and fix, reverify, record, commit.
  - Success criteria: No unresolved in-scope defects, failing checks, or avoidable complexity remain.
  - Verification: <Broadest relevant check and targeted checks after fixes.>
  - Commit target: <Review subject in the configured commit style.>
```

The review uses the last planned subphase label; it does not increment the Phase/Subphase number. Conventional commit targets use `type(scope): summary`; Phase-style targets use `Phase X.Y: description`, or `Phase X.Y Milestone Review: description` for the review. Subjects default to English.

Change each completed item's `[ ]` to `[x]` as soon as its completion and verification requirements are met, including milestone reviews separately. Update the active plan alongside progress and include both in the checkpoint commit. Unfinished, blocked, and cancelled items remain unchecked.

## Completion and resizing

Completion is `incomplete`, `completed`, or `cancelled` (未完成／已完成／已取消). Verify full-goal acceptance and all committed milestone reviews before setting `completed`. Cancellation is explicit user direction and preserves the actual stage completion state.

Use the skill's layout policy to decide when to split or merge documents. Preserve user-added sections and all historical entries during either conversion. Larger structured plans may use a `milestones/` directory with a navigable index; added files and directories are part of the goal and travel with its contents during archiving.

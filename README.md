# Checkpoint Karpathy Agent Workflow

English | [简体中文](README_CN.md)

A Codex + Claude Code workflow for roadmap-driven, checkpointed software development with Karpathy-inspired engineering guardrails.

It is designed for greenfield development, mid-project continuation, feature work, bug fixing, refactoring, late-stage maintenance, and handoffs where work must stay recoverable across quota limits, session resets, and context loss.

## Core idea

Read `config.md` on each use and create it only if missing. Every setting explains its current value, accepted values, effects, and default. Use user-specified settings; otherwise default to collaborative visibility, Conventional Commits, and `auto` layout. Keep recorded settings across goals and change them at the user's request.

Initialization creates the fixed `roadmap/` under the selected state directory and `private/work/` in both modes. Compact layout suits focused goals; structured layout suits larger plans with complex dependencies and evolving context. Both must plan completely to achieve every stated goal.

While a goal is incomplete, the workflow persists across development conversations and resumes its next action. After completion or explicit user cancellation, it deactivates and leaves the documents in place. On the next explicit invocation for a new goal, archive the old contents and initialize new documents inside the same `roadmap/`. Keep configuration and private work.

Each normal subphase must end with:

- a completed roadmap item,
- project-appropriate verification,
- an updated progress log,
- a Git commit,
- and a clear next step.

Commit messages use one of two styles:

Conventional Commits (default):
```text
type(scope): <summary>
```

Phase-style (optional):
```text
Phase X.Y: <description>
```

Description defaults to English. Use another language only when the user asks.

When a major milestone is complete, the agent must perform a standalone milestone review checkpoint before moving on. This checkpoint does not consume the next planned Phase/Subphase number; it confirms scope, simplifies milestone work, runs the broadest relevant verification, reviews for regressions or integration gaps, debugs and fixes in-scope issues, reruns verification, records progress, and commits the closeout.

The engineering guardrails are:

- think before coding,
- keep the solution simple,
- make surgical changes in existing codebases,
- verify against a concrete goal.

## Repository state

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

Create `roadmap/` and `private/work/` during initialization, reusing existing directories. Create archives and work categories when needed. Collaborative mode tracks configuration, goal documents, and archives; privacy mode keeps them under Git-ignored `private/`.

### Configuration

Generate `config.md` with explanations in the user's language. Users edit the `Value` for each setting:

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

On a visibility-mode change, create or reuse the destination `roadmap/`, check conflicts, move active goal contents into it, and move `config.md` into its parent state directory. Preserve the source directory, content, and internal links. Existing archives, private notes, and work stay in place. When switching to privacy, include removal of old tracked active paths in the next relevant commit; existing Git history remains.

### Document layouts

```text
Compact roadmap/
  roadmap.md
  progress.md

Structured roadmap/
  README.md
  status.md
  context.md
  milestones.md
  changelog.md
  progress.md
```

| Content | Compact | Structured |
|---|---|---|
| Goal, overall acceptance, scope, work mode, initial state, navigation | roadmap.md | README.md |
| Completion, current state, phase reference, next action | roadmap.md | status.md |
| Constraints, assumptions, risks, blockers, states and evidence | roadmap.md | context.md |
| Complete milestones, subphases, dependencies, acceptance, verification, commit targets, reviews and completion | roadmap.md | milestones.md |
| Material plan-change reasons, changes and impact | Change log in roadmap.md | changelog.md |
| Actual work, verification results, commits, execution decisions and issue handling | progress.md | progress.md |

Compact layout needs no separate README. Maintain detailed state in one place and reference it using stable identifiers and relative links. Current status is a latest snapshot; histories append. Routine checkbox and next-action updates need no plan-change entry. The next action can be a milestone review or blocker resolution.

With `auto`, assess the whole goal's plan, dependencies, background, design evolution, and accumulated history at planning and during execution. Switch in either direction when useful, avoiding frequent changes. Remaining task count alone does not justify merging. Fixed layouts switch only at the user's request; automatic switches retain `auto` in configuration.

Before switching, back up all original goal files and subdirectories directly into a unique `.checkpoint-karpathy/private/work/backups/roadmap-layout/<timestamp>-<source>-to-<target>/`. Verify the backup. Reorganize by meaning, preserving custom sections, goal, state, identifiers, acceptance, and all history. Check conflicts and links; relocate superseded files individually and compare the result with the backup. Preserve partial output and restore original content on failure. Record the reason, layouts, and backup path in the plan-change log. Layout switching does not archive a goal.

See [roadmap-templates.md](references/roadmap-templates.md) for templates and conversion guidance. Larger documents may be split further by milestone or retrieval needs while retaining complete planning and navigation. Maintained design documents remain in their intended project locations and are referenced by the roadmap.

### Completion and archiving

Record Completion in compact `roadmap.md` or structured `status.md`:

- `incomplete`: Resume the goal. Describe in-progress, paused, or blocked in Current State.
- `completed`: All subphases, reviews, commits, and overall acceptance are satisfied with verification evidence.
- `cancelled`: Explicit user termination or confirmation; record its reason and termination history, preserving unfinished items accurately.

Completed and cancelled goals use the same archive flow on the next invocation for a new goal. Move all contents of `roadmap/`, including added files and subdirectories, directly into `archive/YYYYMMDDa-<old-goal-summary>/`. Increment the date suffix letter to avoid collisions. Archive documents sit directly in this destination, without an extra enclosing `roadmap/` layer.

Keep the fixed `roadmap/` directory and create the new goal files inside it. Retain configuration across archiving and new goals. On resume, read configuration, the actual layout's entry point and completion state, then relevant plans, context, and recent progress. Check completion claims against acceptance and review evidence.

## Temporary work files

Create `.checkpoint-karpathy/private/work/` during initialization in both modes, covered by the `.checkpoint-karpathy/private/` Git ignore rule. It stays in place across mode changes, layout switches, and archiving. Do not automatically archive it or clear it for new goals.

Keep the root free of loose files. Create purpose- or task-specific categories as needed, such as `logs/`, `verification/`, `tools/`, `reports/`, `browser/`, `screenshots/`, `configs/`, `fixtures/`, `backups/`, `drafts/`, `bin/`, and `artifacts/`. Subdivide by task or run when useful.

Manage temporary material separately, retaining useful evidence or tools and cleaning disposable content as needed under project deletion rules. Put durable conclusions and verification summaries in `roadmap/progress.md` so archived documents explain results independently of temporary-file links. Raw evidence may remain in task-specific work directories with paths recorded in progress. Keep maintained source, tests, and user deliverables in their intended project locations.

## Install for Codex

Copy the skill into Codex's project or user skill directory:

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp -R .codex/skills/checkpoint-karpathy-development/. ~/.codex/skills/checkpoint-karpathy-development/
```

For project-level Codex instructions, copy:

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

Use it:

```text
$checkpoint-karpathy-development

Read AGENTS.md and read or create config.md. Use its visibility mode, commit message style, and layout policy, create or update the complete goal plan inside roadmap/, complete one roadmap subphase, update progress, run project-appropriate verification, and git commit.
```

## Install for Claude Code

For project-level Claude Code instructions, copy:

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
```

Copy the Claude Code skill:

```bash
mkdir -p /path/to/your/project/.claude/skills/checkpoint-karpathy-development
cp -R .claude/skills/checkpoint-karpathy-development/. /path/to/your/project/.claude/skills/checkpoint-karpathy-development/
```

Optional slash command:

```bash
mkdir -p /path/to/your/project/.claude/commands
cp .claude/commands/checkpoint-karpathy.md /path/to/your/project/.claude/commands/checkpoint-karpathy.md
```

Use it:

```text
/checkpoint-karpathy Continue this project using checkpoint-karpathy development. Select the work mode, update the roadmap, complete one subphase, update progress, verify, and commit.
```

## Gitignore

Add one line to `.gitignore`:

```gitignore
.checkpoint-karpathy/private/
```

In privacy mode, configuration, `roadmap/`, and archives are under `private/`. In both modes the same rule covers work, backups, and sensitive notes.

Do not ignore `.checkpoint-karpathy/` wholesale unless you intentionally want to hide all workflow state.

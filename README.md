# Checkpoint Karpathy Agent Workflow

English | [简体中文](README_CN.md)

[Installation](#installation) | [Agent installation guide](INSTALL.md)

Roadmap-driven, checkpointed software development with Karpathy-inspired engineering guardrails. Works with Codex, Claude Code, Pi, Oh My Pi, Antigravity, Cursor, DeepSeek Harness, and other compatible agents.

It is designed for greenfield development, mid-project continuation, feature work, bug fixing, refactoring, late-stage maintenance, and handoffs where work must stay recoverable across quota limits, session resets, and context loss.

## Core idea

Read `config.md` on each use and create it only if missing. Every setting explains its current value, accepted values, effects, and default. Use user-specified settings; otherwise default to collaborative visibility and Conventional Commits. Keep recorded settings across goals and change them at the user's request.

Initialization creates the fixed `roadmap/` under the selected state directory and `private/work/` in both modes. Goal documents live inside `roadmap/`, with separate overview, status, context, milestone plan, plan-change history, and execution history. The initial plan must cover every stated goal completely.

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
```

On a visibility-mode change, create or reuse the destination `roadmap/`, check conflicts, move active goal contents into it, and move `config.md` into its parent state directory. Preserve the source directory, content, and internal links. Existing archives, private notes, and work stay in place. When switching to privacy, include removal of old tracked active paths in the next relevant commit; existing Git history remains.

### Roadmap documents

```text
roadmap/
  README.md
  status.md
  context.md
  milestones.md
  changelog.md
  progress.md
```

| Document | Content |
|---|---|
| README.md | Goal, overall acceptance, scope, work mode, initial state, navigation |
| status.md | Completion, current state, phase reference, next action |
| context.md | Constraints, assumptions, risks, blockers, states and evidence |
| milestones.md | Complete milestones, subphases, dependencies, acceptance, verification, commit targets, reviews and completion |
| changelog.md | Material plan-change reasons, changes and impact |
| progress.md | Actual work, verification results, commits, execution decisions and issue handling |

Create all six files, keeping entries proportional to the goal. Maintain detailed state in one place and reference it using stable identifiers and relative links. Current status is a latest snapshot; histories append. Routine checkbox and next-action updates need no plan-change entry. The next action can be a milestone review or blocker resolution.

On resume, read `README.md`, `status.md`, recent progress, and the active milestone with relevant context and dependencies. Read plan-change history when needed to understand a decision. Review the complete plan for scope or cross-milestone dependency changes and final acceptance. Routine checkpoints update milestone checkboxes, status, and progress together; update other documents when their information changes.

See [roadmap-templates.md](references/roadmap-templates.md) for document templates. Larger documents may be split further by milestone or retrieval needs while retaining complete planning and navigation. Maintained design documents remain in their intended project locations and are referenced by the roadmap.

### Completion and archiving

Record Completion in `roadmap/status.md`:

- `incomplete`: Resume the goal. Describe in-progress, paused, or blocked in Current State.
- `completed`: All subphases, reviews, commits, and overall acceptance are satisfied with verification evidence.
- `cancelled`: Explicit user termination or confirmation; record its reason and termination history, preserving unfinished items accurately.

Completed and cancelled goals use the same archive flow on the next invocation for a new goal. Move all contents of `roadmap/`, including added files and subdirectories, directly into `archive/YYYYMMDDa-<old-goal-summary>/`. Increment the date suffix letter to avoid collisions. Archive documents sit directly in this destination, without an extra enclosing `roadmap/` layer.

Keep the fixed `roadmap/` directory and create the new goal files inside it. Retain configuration across archiving and new goals. On resume, read configuration, `roadmap/README.md`, and `roadmap/status.md`, then relevant plans, context, and recent progress. Check completion claims against acceptance and review evidence.

## Temporary work files

Create `.checkpoint-karpathy/private/work/` during initialization in both modes, covered by the `.checkpoint-karpathy/private/` Git ignore rule. It stays in place across mode changes and archiving. Do not automatically archive it or clear it for new goals.

Keep the root free of loose files. Create purpose- or task-specific categories as needed, such as `logs/`, `verification/`, `tools/`, `reports/`, `browser/`, `screenshots/`, `configs/`, `fixtures/`, `backups/`, `drafts/`, `bin/`, and `artifacts/`. Subdivide by task or run when useful.

Manage temporary material separately, retaining useful evidence or tools and cleaning disposable content as needed under project deletion rules. Put durable conclusions and verification summaries in `roadmap/progress.md` so archived documents explain results independently of temporary-file links. Raw evidence may remain in task-specific work directories with paths recorded in progress. Keep maintained source, tests, and user deliverables in their intended project locations.

## Skill organization

[SKILL.md](SKILL.md) contains the execution workflow, required constraints, and links to details at the operation that needs them. Read the relevant reference before that operation:

- [Project state](references/project-state.md): configuration, initialization, visibility-mode changes, and archiving.
- [Roadmap templates](references/roadmap-templates.md): document responsibilities and goal templates.
- [Checkpoint details](references/checkpoint-details.md): progress templates, milestone reviews, and verification discovery.

Install the complete skill directory, including `references/`.

## Installation

Install interactively and select your harness and scope:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development-skills/main/install.sh | bash
```

Or specify the harness directly:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development-skills/main/install.sh | bash -s -- --harness codex --scope user
```

Supports `claude`, `codex`, `pi`, `ohmypi`, `antigravity`, `cursor`, `deepseek`, `gemini`, and `opencode`. Use `--harness claude,cursor` for multiple harnesses, or `--project /path/to/project` for project installation. For a local checkout, run `bash install.sh --harness codex --source .`.

### Let your agent install it

Send your agent the repository link with an installation request, for example:

```text
Install this skill for my current harness:
https://github.com/yjrszcq/checkpoint-karpathy-development-skills
Follow INSTALL.md in the repository.
```

[INSTALL.md](INSTALL.md) provides agent instructions, supported paths, custom-directory options, updates, backups, and verification. The installer uses the root `SKILL.md` and complete `references/` as its package source. It preserves existing project instructions and backs up previous installations outside skill discovery.

After installation, restart or reload your harness and ask it to use `checkpoint-karpathy-development` for your goal.

## Gitignore

Add one line to `.gitignore`:

```gitignore
.checkpoint-karpathy/private/
```

In privacy mode, configuration, `roadmap/`, and archives are under `private/`. In both modes the same rule covers work, backups, and sensitive notes.

Do not ignore `.checkpoint-karpathy/` wholesale unless you intentionally want to hide all workflow state.

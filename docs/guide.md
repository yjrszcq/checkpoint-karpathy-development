# Usage guide

[简体中文](guide_CN.md) | [Project home](../README.md)

## Installation

Install interactively and select your harness and scope:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash
```

Or specify the harness directly:

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash -s -- --harness codex --scope user
```

### Harness identifiers

| Harness | `--harness` value |
|---|---|
| Claude Code | `claude` |
| Codex | `codex` |
| Pi | `pi` |
| Oh My Pi | `ohmypi` |
| Antigravity | `antigravity` |
| Cursor | `cursor` |
| DeepSeek Harness | `deepseek` |
| Gemini CLI | `gemini` |
| OpenCode | `opencode` |
| Custom | `custom` |

Use `--harness claude,cursor` for multiple harnesses, or `--project /path/to/project` for project installation. For a local checkout, run `bash install.sh --harness codex --source .`.

Select `custom` in the interactive menu to enter a skills directory manually, or pass `--harness custom --skills-dir /actual/path/to/skills`. The installer creates `checkpoint-karpathy-development/` inside that directory.

### Let your agent install it

Send your agent the repository link with an installation request, for example:

```text
Install this skill for my current harness:
https://github.com/yjrszcq/checkpoint-karpathy-development
Follow INSTALL.md in the repository.
```

[INSTALL.md](../INSTALL.md) provides agent instructions, supported paths, custom-directory options, updates, backups, and verification. The installer uses the root `SKILL.md`, `LICENSE`, and complete `references/`, `scripts/`, and `assets/` as its package source. It backs up previous installations outside skill discovery.

After installation, restart or reload your harness and ask it to use `checkpoint-karpathy-development` for your goal.

## Core idea

Read `config.yaml` on each use and create it only if missing. Every setting explains its current value, accepted values, effects, and default. Use user-specified settings; otherwise default to collaborative visibility and Conventional Commits. Keep recorded settings across goals and change them at the user's request.

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

When a major milestone is complete, the agent must perform a standalone milestone review checkpoint before moving on. It uses the last planned phase label with a review suffix, confirms scope, simplifies milestone work, runs the broadest relevant verification, reviews for regressions or integration gaps, debugs and fixes in-scope issues, reruns verification, records progress, and commits the closeout.

The engineering guardrails are:

- think before coding,
- keep the solution simple,
- make surgical changes in existing codebases,
- verify against a concrete goal.

## Repository state

**Collaborative mode:**
```text
.checkpoint-karpathy/
  config.yaml
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
    roadmap/
    work/
    archive/
```

Create `roadmap/` and `private/work/` during initialization, reusing existing directories. Create archives and work categories when needed. Collaborative mode tracks configuration, goal documents, and archives; privacy mode keeps them under Git-ignored `private/`.

### Configuration

Generate `config.yaml` with explanations in the user's language. Users edit the YAML values; comments explain each setting:

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

On a visibility-mode change, create or reuse the destination `roadmap/`, check conflicts, move active goal contents into it, and move `config.yaml` into its parent state directory. Preserve the source directory, content, and internal links. Existing archives, private notes, and work stay in place. When switching to privacy, include removal of old tracked active paths in the next relevant commit; existing Git history remains.

### Project-state commands

The project-state helpers require **Python 3.9+** and **PyYAML >= 6.0**. Before using them, install dependencies in the Python environment that will run the scripts:

```bash
python3 -m pip install -r /path/to/skill/scripts/requirements.txt
```

Run the installed scripts with the actual project root:

```bash
python3 /path/to/skill/scripts/init_project.py --project /path/to/project --mode collaborative --language en
# Send complete structured JSON on stdin; see the input example linked below.
python3 /path/to/skill/scripts/create_goal.py --project /path/to/project
python3 /path/to/skill/scripts/archive_goal.py --project /path/to/project --title old-goal-summary
```

Initialization creates annotated YAML configuration, fixed empty directories, and the private Git ignore rule. Use `--mode privacy` or `--commit-message-style phase` for user-selected initial settings. Existing configuration and complete goal documents are preserved; recover partial state first. The agent sends structured JSON on standard input to `create_goal.py`, which validates content and fills templates to generate six actual documents with unchecked plan items. It records roadmap generation in progress and the initial plan baseline in changelog. Read [structured goal input](../references/goal-input.md) for the complete schema and invocation. Before replacing a terminal goal, validate new content with `--check-only`, archive the old goal, then run creation with the same input. Archiving reads configuration, moves the goal contents, and leaves the fixed roadmap directory empty. Configuration and work persist. See [helper commands](../references/project-state.md#helper-commands) for status and recovery.

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

See [roadmap-templates.md](../references/roadmap-templates.md) for document templates. Larger documents may be split further by milestone or retrieval needs while retaining complete planning and navigation. Maintained design documents remain in their intended project locations and are referenced by the roadmap.

### Completion and archiving

Record Completion in `roadmap/status.md`:

- `incomplete`: Resume the goal. Describe in-progress, paused, or blocked in Current State.
- `completed`: All subphases, reviews, commits, and overall acceptance are satisfied with verification evidence.
- `cancelled`: Explicit user termination or confirmation; record its reason and termination history, preserving unfinished items accurately.

Completed and cancelled goals use the same archive flow on the next invocation for a new goal. Move all contents of `roadmap/`, including added files and subdirectories, directly into `archive/YYYYMMDDa-<old-goal-summary>/`. Increment the date suffix letter to avoid collisions.

Keep the fixed `roadmap/` directory and create the new goal files inside it. Retain configuration across archiving and new goals.

## Temporary work files

Create `.checkpoint-karpathy/private/work/` during initialization in both modes, covered by the `.checkpoint-karpathy/private/` Git ignore rule. It stays in place across mode changes and archiving. Do not automatically archive it or clear it for new goals.

Keep the root free of loose files. Create purpose- or task-specific categories as needed, such as `logs/`, `verification/`, `tools/`, `reports/`, `browser/`, `screenshots/`, `configs/`, `fixtures/`, `backups/`, `drafts/`, `bin/`, and `artifacts/`. Subdivide by task or run when useful.

Manage temporary material separately, retaining useful evidence or tools and cleaning disposable content as needed under project deletion rules. Put durable conclusions and verification summaries in `roadmap/progress.md` so archived documents explain results independently of temporary-file links. Raw evidence may remain in task-specific work directories with paths recorded in progress. Keep maintained source, tests, and user deliverables in their intended project locations.

## Skill organization

[SKILL.md](../SKILL.md) contains the execution workflow, required constraints, and links to details at the operation that needs them. Read the relevant reference before that operation:

- [Project state](../references/project-state.md): configuration, initialization, visibility-mode changes, and archiving.
- [Structured goal input](../references/goal-input.md): fields, validation, and JSON invocation examples.
- [Roadmap templates](../references/roadmap-templates.md): document responsibilities and goal templates.
- [Checkpoint details](../references/checkpoint-details.md): progress templates, milestone reviews, and verification discovery.

## Gitignore

Add one line to `.gitignore`:

```gitignore
.checkpoint-karpathy/private/
```

In privacy mode, configuration, `roadmap/`, and archives are under `private/`. In both modes the same rule covers work, backups, and sensitive notes.

Do not ignore `.checkpoint-karpathy/` wholesale unless you intentionally want to hide all workflow state.

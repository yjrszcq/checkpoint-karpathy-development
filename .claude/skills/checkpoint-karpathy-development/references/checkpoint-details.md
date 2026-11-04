# Checkpoint details

Read the progress template before creating or reconstructing a progress log. Read the milestone review procedure before each review. Use the verification section when project checks are unclear. Paths illustrating `.checkpoint-karpathy/` resolve under the configured state directory in privacy mode.

## Progress template

Use this structure in the active `roadmap/progress.md`, under the state directory selected by configuration:

```md
# Checkpoint Karpathy Progress

## Phase <N or M.S>: <short title>

Date: <YYYY-MM-DD>
Roadmap item: <milestone/subphase reference>
Commit: <hash after commit, or pending before commit>

### Goal
<What this phase was meant to accomplish.>

### Completed
- <Concrete completed item>

### Files Changed
- `<path>` — <why it changed>

### Verification
- `<command or method>` — <result>
- If not run: <reason>

### Decisions
- <Important technical decision and rationale>

### Known Issues
- <Open issue, limitation, or risk>
- If none: None known.

### Next Step
<The next roadmap subphase or a roadmap update.>
```

For a milestone review checkpoint, use a non-incrementing phase label and include:

```md
## Phase <last planned phase> Milestone Review: <short title>

Date: <YYYY-MM-DD>
Roadmap item: Milestone <N> Review after Phase <last planned phase>
Commit: <hash after commit, or pending before commit>

### Goal
<What the milestone review was meant to stabilize.>

### Closeout Order
- Scope and evidence: <confirmed milestone goal and touched surface>
- Simplification: <what was simplified or why no simplification was needed>
- Broad verification: <initial broad checks and results>
- Review findings: <findings and outcomes>
- Debugging / fixes: <bugs found and fixed, or none>
- Final verification rerun: <failed checks and broad checks rerun after fixes>
```

Append entries. Do not erase useful prior history.

## Milestone review

When all planned subphases in a major milestone are complete, perform a standalone milestone review checkpoint before starting the next milestone or declaring the goal done.

The milestone review is separate from the final planned subphase. It must update `.checkpoint-karpathy/roadmap/progress.md` and have its own commit, but it does not consume or increment the planned Phase/Subphase number. Reuse the last completed planned phase label with a review suffix, such as:

```md
## Phase 1.2 Milestone Review: stabilize authentication flow
```

Do not label this checkpoint as `Phase 1.3` unless `1.3` is an actual planned roadmap subphase.

Use this order for the milestone review:

1. Confirm scope and evidence: restate what the milestone was meant to accomplish and which touched surfaces need review.
2. Simplify: remove speculative abstractions, unnecessary layers, unused frameworks, unused files, unused imports, and dead paths introduced by the milestone.
3. Run broad verification: run the broadest project-appropriate verification available for the milestone's touched surface, plus targeted checks for changed behavior.
4. Review: inspect the whole milestone for regressions, inconsistent behavior, missing tests, stale documentation, roadmap drift, and integration gaps.
5. Debug and fix: reproduce every failing check or discovered defect that is in scope, isolate the cause, and fix it.
6. Rerun verification: rerun the failed checks and the broad milestone verification after fixes.
7. Record and commit: update progress with the review results, update the roadmap if needed, review diffs, and commit the milestone review checkpoint.

Preserve existing behavior unless the user requested a change, and avoid unrelated refactors. Do not mark the milestone complete until simplification, verification results, review findings, debugging, fixes, and final rerun results are recorded in `.checkpoint-karpathy/roadmap/progress.md`. If a blocking issue cannot be fixed in the review checkpoint, update the roadmap, record the blocker in progress, and commit only a coherent checkpoint that leaves the repository understandable.

## Verification discovery

Never assume the project stack.

Before running checks, inspect:

- `README.md`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, docs,
- `package.json`, lockfiles,
- `pyproject.toml`, Python config files,
- `Cargo.toml`,
- `go.mod`,
- `pom.xml`, `build.gradle`,
- `.csproj`, `.sln`,
- `CMakeLists.txt`, `Makefile`, `meson.build`,
- `Gemfile`,
- `composer.json`,
- `Package.swift`,
- `Dockerfile`, compose files,
- `justfile`, `Taskfile.yml`.

Prefer project-declared commands over generic guesses.

Use the smallest relevant check:

- test,
- build,
- type check,
- lint,
- format check,
- compile check,
- smoke check,
- manual inspection if no command exists.

If no reliable verification exists yet, write that explicitly in progress.

Do not pretend a check passed.

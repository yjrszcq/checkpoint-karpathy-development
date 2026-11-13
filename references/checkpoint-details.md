# Checkpoint details

Read the progress template before creating or reconstructing a progress log. Read the milestone review procedure before each review. Use the verification section when project checks are unclear. Paths illustrating `.checkpoint-karpathy/` resolve under the configured state directory in privacy mode.

## Progress template

The creation script records roadmap generation as the first execution entry. Subsequent entries record actual work and evidence; append them chronologically and preserve useful prior history. Use concise labelled paragraphs or sections in the user's language, keeping the date, stable roadmap reference, commit, completed work, verification, remaining scope, and next step easy to find.

Verification records must make the evidence's scope clear: what was checked, the observed result, and which revision or inputs it covers where that affects the conclusion. Distinguish rerun checks from reused evidence and record limitations. Link to detailed logs in private work when useful, keeping the durable outcome in progress. Keep shared progress free of sensitive details. A completed subphase supports checking that item in milestones.md; parent milestones and full-goal acceptance still require their own evidence. Keep the latest state and next action in status.md. When work reveals a reusable project lesson, record its concise conclusion, scope, and useful evidence in project-level `memory.md`; keep the investigation history here.

### Execution entry

```md
## <YYYY-MM-DD> · <roadmap item ID>: <short title>

Commit: <hash after commit, or pending before commit>

Goal: <Intended outcome and scope of this checkpoint.>

Completed: <Concrete changes and resulting behavior; name relevant files or
interfaces where they help the next agent locate the work.>

Verification:
- `<command or method>` — <observed result and coverage; link to useful evidence>
- <For reused evidence, identify its source and why it still applies. For omitted
  checks, record the reason and resulting limitation.>

Boundaries / remaining: <Unmet acceptance criteria, known issues, or parent
milestone work still open, with roadmap/context links where useful. A completed
subphase alone does not establish parent milestone or full-goal completion.>

Next: <Next roadmap item or blocker-resolution action. Keep the current snapshot
and next action updated in status.md; this entry records the handoff at this point.>

```

Add the following only when relevant:

```md
Decision: <Choice and rationale; link to the maintained design or plan change.>

Failure / recovery: <What failed, cause or remaining uncertainty, correction,
and retest result.>

Ongoing check: <Command, tested revision/input, process or session handle, log
path, last observed state, and how to inspect or resume it. Record the terminal
result when observed; a running check is not a pass.>

```

For a milestone review, use the following heading and metadata in place of the
normal entry heading and metadata. Include Closeout Order alongside the shared
Goal, Completed, Verification, Boundaries / remaining, and Next fields above.
Reuse the last planned phase label.

```md
## <YYYY-MM-DD> · Phase <last planned phase> Milestone Review: <short title>

Roadmap item: Milestone <N> Review after Phase <last planned phase>
Commit: <hash after commit, or pending before commit>

### Closeout Order
- Scope and evidence: <confirmed milestone goal and touched surface>
- Simplification: <what was simplified or why no simplification was needed>
- Broad verification: <initial broad checks and results>
- Review findings: <findings and outcomes>
- Debugging / fixes: <bugs found and fixed, or none>
- Final verification rerun: <failed checks and broad checks rerun after fixes>
```

## Milestone review

When all planned subphases in a major milestone are complete, perform a standalone milestone review checkpoint before starting the next milestone or declaring the goal done.

Give the milestone review its own progress entry and commit. Reuse the last completed planned phase label with a review suffix, such as:

```md
## Phase 1.2 Milestone Review: stabilize authentication flow
```

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

# Structured goal input

Read before generating a new roadmap. The agent supplies actual planning content as JSON on standard input; `create_goal.py` validates it and renders the templates in [assets/roadmap/](../assets/roadmap/). The script controls document structure, unchecked plan items, review structure, initial completion, and initial records. Content completeness and realistic acceptance remain the agent's responsibility.

## Invocation and content

Initialize the project directories and configuration first. Send one complete JSON object per invocation. A quoted heredoc preserves literal shell characters in content; encode newlines and quotes according to JSON syntax. For large input, use a tool's subprocess standard-input argument where available. Keep a reusable payload in a task-specific private work directory when validating before archiving; the script receives the payload as JSON bytes on standard input.

```bash
python3 /path/to/skill/scripts/create_goal.py --project /path/to/project <<'JSON'
{
  "language": "en",
  "goal": "Add session login with reliable expiration.",
  "acceptance": [
    "A valid login opens a session, and an expired session cannot access protected routes; verify with integration tests."
  ],
  "included": ["Session creation, expiration, protected-route checks, and relevant tests."],
  "non_goals": ["Changing account registration."],
  "work_mode": "feature",
  "initial_state": "Existing account validation works; session support is absent.",
  "current_state": "Ready to implement the session flow.",
  "next_action": "Implement 1.1, then verify its success criteria.",
  "context": {
    "constraints": ["Preserve existing account validation behavior."],
    "assumptions": ["Unverified: existing test fixtures can exercise route authentication; confirm while inspecting route tests."],
    "risks": [],
    "blockers": []
  },
  "milestones": [
    {
      "id": "1",
      "title": "Deliver session login",
      "purpose": "Provide the complete authenticated session flow.",
      "dependencies": [],
      "phases": [
        {
          "id": "1.1",
          "title": "Implement and verify the session flow",
          "dependencies": [],
          "scope": "Session creation, expiry, route authorization, and regression tests.",
          "success_criteria": "Valid sessions reach protected routes; absent or expired sessions are rejected; existing account validation still passes.",
          "verification": "Run the project's session and protected-route integration tests, including expiry boundary cases.",
          "commit": "feat(auth): add expiring login sessions"
        }
      ],
      "review": {
        "verification": "Run the complete authentication regression suite and review integration boundaries and overall acceptance.",
        "commit": "chore(review): verify session login delivery"
      }
    }
  ]
}
JSON
```

This example illustrates structure, not the required size of a plan. Include every milestone and commit-sized subphase needed for the actual goal. Discover real project checks before supplying verification content.

## Field rules

- All top-level fields shown are required except `language`, which defaults to `en`. `language` accepts `en` or `zh` and controls generated roadmap-generation and initial-plan record prose. Write supplied content in the user's language. Template section labels remain stable English labels.
- `goal`, `initial_state`, `current_state`, and `next_action` are nonempty strings. `work_mode` is `greenfield`, `continuation`, `feature`, `bugfix`, `refactor`, or `maintenance`.
- `acceptance` and `included` are nonempty arrays of nonempty strings; `non_goals` is an array that may be empty. Include observable full-goal criteria and their verification methods in `acceptance`.
- `context` contains exactly `constraints`, `assumptions`, `risks`, and `blockers`, each an array of nonempty strings or `[]`. The script prefixes entries with `C-01`, `A-01`, `R-01`, or `B-01`; do not repeat that prefix in supplied text. Include relevant rationale, status, validation, impact, response, and evidence links in the text.
- `milestones` is nonempty. Each milestone contains exactly `id`, `title`, `purpose`, `dependencies`, `phases`, and `review`. `phases` is nonempty; each phase contains exactly `id`, `title`, `dependencies`, `scope`, `success_criteria`, `verification`, and `commit`. Other than the arrays/objects, these fields are nonempty strings; titles fit on one line.
- IDs are globally unique across milestones and subphases. Use letters, numbers, dots, underscores, and hyphens, beginning with a letter or number. Dependencies are arrays of IDs from the complete plan, or `[]`. List milestones and their phases in execution order: each dependency must finish before the dependent item starts. A milestone ID represents completion of that milestone including its review, so a phase cannot depend on its own parent milestone. Unknown IDs, self references, cycles, and dependencies on later work are rejected.
- Each `review` contains exactly `verification` and `commit`, both nonempty strings. The script generates a separate unchecked review after the milestone's subphases, with the last phase's label and the required closeout sequence.
- `commit` is the full subject in the configured style. For `conventional`, use `type(scope): summary`; for `phase`, use `Phase <phase ID>: summary`, and `Phase <last phase ID> Milestone Review: summary` for reviews. Subjects default to English unless the user requests another language.
- Strings may contain multiline prose and inline Markdown. JSON object keys must be unique. Unknown fields, missing fields, empty required content, invalid IDs, and incorrectly styled commit targets are errors; they are not silently discarded.

The script derives Current Phase from the first subphase, Completion as `incomplete`, and all checkboxes as unchecked. It generates context IDs and navigation links. The first progress entry records roadmap generation and structural validation only; the first changelog entry establishes the initial plan baseline. Do not supply completion flags, execution history, or fabricated test results. Creating directories and `config.yaml` is not recorded in these goal logs.

## Validate, archive, create

`create_goal.py --check-only` accepts the same JSON. It validates and renders without writing and can run while a previous goal still occupies `roadmap/`. Use it before archiving a terminal goal for replacement. After successful validation and evidence review, run `archive_goal.py`, then `create_goal.py` with the same content. Creation refuses a nonempty `roadmap/`; recover partial state instead of retrying blindly.

For first use, run initialization followed by creation. Continuing an active goal requires ordinary document updates, not recreation. An explicit archive-only request runs the archive command without creating a new goal. See [Helper commands](project-state.md#helper-commands) for configuration, paths, and failure recovery.

---
description: Run checkpoint-karpathy development for a multi-step coding task
argument-hint: [task]
---

Use checkpoint-karpathy development for this task: $ARGUMENTS

Follow the project `CLAUDE.md` and, if available, the skill at `.claude/skills/checkpoint-karpathy-development/SKILL.md`.

Mandatory workflow:
1. Select work mode: greenfield, continuation, feature, bug fix, refactor, or maintenance.
2. Define the current phase goal.
3. Inspect repository state and run `git status` before editing.
4. Implement one minimal coherent phase.
5. Detect the project stack before selecting verification.
6. Run the smallest relevant project-appropriate verification, or document why no check exists.
7. Update `docs/progress.md`.
8. Keep scratch/intermediate files under `.agent-artifacts/` and ensure it is gitignored.
9. Review `git status`, `git diff`, and `git diff --staged`.
10. Commit the completed phase.

Do not leave completed phase work uncommitted. Do not commit unrelated user changes. Do not run destructive Git commands without explicit permission.

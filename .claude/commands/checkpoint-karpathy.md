---
description: "Run checkpoint-karpathy development for one commit-sized roadmap subphase."
---

Use checkpoint-karpathy development for the requested task.

Instructions:

1. Read project instructions, including `CLAUDE.md` and `AGENTS.md` if present.
2. **Re-invocation check:** If `.checkpoint-karpathy/roadmap.md` (or `.checkpoint-karpathy/private/roadmap.md` in privacy mode) already exists:
   - If the roadmap is already complete, archive it to `.checkpoint-karpathy/archive/YYYY-MM-DD-<summary>/` (or `.checkpoint-karpathy/private/archive/YYYY-MM-DD-<summary>/` in privacy mode), then create a fresh roadmap and progress for the new goal.
   - If the roadmap is not yet complete, continue from the next unfinished subphase.
3. Select the work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
4. Create or update the roadmap. The initial roadmap must plan completely to achieve all stated goals.
5. Complete exactly one commit-sized roadmap subphase, or one standalone milestone review checkpoint if a major milestone is complete.
6. For normal subphases, run the smallest project-appropriate verification.
7. For milestone review checkpoints, do not increment the planned Phase/Subphase number; confirm scope, simplify milestone work, run the broadest relevant verification, review for regressions or integration gaps, debug and fix in-scope issues, and rerun verification.
8. Update progress.
9. Run `git status`, `git diff`, stage relevant files only, run `git diff --staged`, and commit with an English Conventional Commits-style message unless the user requested another language.
10. Report the commit and the next subphase.
11. **Continue until done:** If there are more subphases remaining, proceed to the next one. If the roadmap is fully complete, report goal completion and stop using this skill.

User request:

$ARGUMENTS

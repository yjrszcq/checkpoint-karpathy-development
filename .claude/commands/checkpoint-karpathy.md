---
description: "Run checkpoint-karpathy development for one commit-sized roadmap subphase."
---

Use checkpoint-karpathy development for the requested task.

Instructions:

1. Read project instructions, including `CLAUDE.md` and `AGENTS.md` if present. Look for `config.md` in `.checkpoint-karpathy/` and `.checkpoint-karpathy/private/`; read the active configuration, or create it before roadmap and progress files using user-specified settings and defaults for anything unspecified (`Mode: collaborative`, `Commit message style: conventional`). If both configurations exist, ask which one to keep. Apply user-requested settings changes, moving the active three files together when the mode changes and following its Git tracking policy. Preserve existing state on destination conflicts.
2. **Re-invocation check:** Check if `roadmap.md` exists in the directory selected by `config.md`.
   - **No roadmap:** Proceed to step 3 using the recorded settings.
   - **Roadmap is complete:** Archive it to `.checkpoint-karpathy/archive/YYYYMMDDa-<summary>/` (or `.checkpoint-karpathy/private/archive/YYYYMMDDa-<summary>/` in privacy mode). `<summary>` describes the **completed goal being archived** (read it from the old roadmap), not the new one. The letter auto-increments to avoid same-day collisions. Keep `config.md` active, then create a fresh roadmap and progress for the new goal.
   - **Roadmap is not yet complete:** Resume from the next unfinished subphase.
3. Select the work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance.
4. Create or update the roadmap. The initial roadmap must plan completely to achieve all stated goals.
5. Complete exactly one commit-sized roadmap subphase, or one standalone milestone review checkpoint if a major milestone is complete.
6. For normal subphases, run the smallest project-appropriate verification.
7. For milestone review checkpoints, do not increment the planned Phase/Subphase number; confirm scope, simplify milestone work, run the broadest relevant verification, review for regressions or integration gaps, debug and fix in-scope issues, and rerun verification.
8. Update progress.
9. Run `git status`, `git diff`, stage relevant files only, run `git diff --staged`, and commit using the style recorded in `config.md` (`conventional` for Conventional Commits, `phase` for Phase-style; description defaults to English).
10. Report the commit and the next subphase.
11. **Continue until done:** If there are more subphases remaining, proceed to the next one within this conversation. If this conversation ends, the next development conversation should automatically resume this skill from the next unfinished subphase. If the roadmap is fully complete, report goal completion — the skill is no longer active.

User request:

$ARGUMENTS

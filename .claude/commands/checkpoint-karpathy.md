---
description: "Run checkpoint-karpathy development through commit-sized subphases and milestone reviews."
---

Use checkpoint-karpathy development for the requested task. Read its SKILL.md and the relevant document templates when initializing or switching layouts.

Instructions:

1. Read project instructions, including `CLAUDE.md` and `AGENTS.md` if present. Look for `config.md` in `.checkpoint-karpathy/` and `.checkpoint-karpathy/private/`. Read the active configuration; resolve duplicate configurations with the user. Create it only if missing, using user-specified settings and defaults for anything unspecified: collaborative visibility, conventional commit messages, and auto roadmap layout. Explain every setting's purpose, accepted values and effects, and default in the user's language. Retain configuration across goals and archives; change settings only at the user's request.
2. Initialize the selected state directory and its fixed `roadmap/`, plus `.checkpoint-karpathy/private/work/` in both modes. Ignore `.checkpoint-karpathy/private/` in Git. Keep temporary files in purpose- or task-specific subdirectories, with no loose files at the work root. Keep work and its contents across goals, mode changes, layout changes, and archiving.
3. Apply user-requested settings changes. For a visibility-mode change, create or reuse the destination `roadmap/`, move active goal contents into it, and move `config.md` into its parent state directory without overwriting state; keep the source directory, preserve links, and apply the selected tracking policy. Existing archives, private notes, and work stay in place. Update uncompleted commit targets for a commit-style change.
4. Inspect the actual layout and Completion: compact uses `roadmap/roadmap.md` and `roadmap/progress.md`; structured uses `roadmap/README.md`, `status.md`, `context.md`, `milestones.md`, `changelog.md`, and `progress.md`. Record Completion in the compact roadmap or structured status.
   - **No goal documents:** Select a layout and plan from scratch. Preserve and recover partial or misplaced state rather than discarding it.
   - **incomplete:** Resume the next unfinished action, which may be a subphase, milestone review, or blocker resolution. Paused and blocked remain incomplete.
   - **completed:** Check all subphases, review commits, and overall acceptance evidence before treating completion as final.
   - **cancelled:** Require explicit user direction or confirmation; record the reason and termination in progress, preserving unfinished items accurately.
   - **completed or cancelled, and starting a new goal:** Move all contents of `roadmap/` directly into an unused `archive/YYYYMMDDa-<old-goal-summary>/` under the selected state directory. Include extra files and subdirectories, preserve links, and increment the letter to avoid collisions. Keep the fixed `roadmap/`, configuration, and work; initialize the new goal inside `roadmap/` after archiving succeeds. Archive contents have no enclosing `roadmap/` layer.
5. Under auto layout, assess the whole goal's complete plan, dependencies, context, design evolution, and history; choose and reassess either layout. Remaining task count alone does not justify switching. Fixed compact or structured layouts switch only at the user's request. Keep auto in configuration after an automatic switch.
6. Before a layout switch, copy all original goal contents directly into a unique `.checkpoint-karpathy/private/work/backups/roadmap-layout/<timestamp>-<source>-to-<target>/` and verify completeness. Interpret documents by meaning even when headings differ. Preserve all custom content, state, IDs, acceptance, and history; check conflicts, update links, and compare the result with the backup. Relocate superseded files individually to a separate backup subdirectory. Preserve failed output separately and restore the original content on failure. Record the reason, layouts, and backup path in the active plan-change log. Switching does not archive a goal.
7. Select the work mode: greenfield, continuation, feature, bugfix, refactor, or maintenance. Create or update the complete goal plan, including all milestones, commit-sized subphases, dependencies, acceptance, verification, commit targets, and standalone milestone reviews.
8. Complete one commit-sized subphase or one milestone review per iteration. Normal subphases use the smallest project-appropriate verification. Milestone reviews confirm scope, simplify, verify broadly, review for regressions or integration gaps, debug and fix in-scope issues, and reverify. Reuse the last planned phase label with a review suffix; do not increment the Phase/Subphase number.
9. Update the active plan checkbox and latest status and next action; append actual work and verification to progress. Maintain detailed context in one place and append material plan changes and their reasons to the plan-change log. On the final review, verify overall acceptance and set Completion to completed in the closeout commit.
10. Run `git status` and `git diff`, stage relevant files only, run `git diff --staged`, and commit using the recorded style: conventional or phase. Descriptions default to English. Report the commit and next action.
11. Continue to the next action while the goal is incomplete, until the conversation ends or the user pauses or cancels work. Resume automatically in the next development conversation. After completion or cancellation, deactivate the skill and leave the documents in place; use it for a new goal only when explicitly invoked.

User request:

$ARGUMENTS

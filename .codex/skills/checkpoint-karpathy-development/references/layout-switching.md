# Layout switching

Read this procedure and [Roadmap templates](roadmap-templates.md) before converting an active goal between layouts. Read the existing goal documents before judging whether conversion helps.

## Selection criteria

Visibility mode, commit style, and roadmap layout are separate settings.

- `auto`: Choose a layout for each new goal and reassess during execution. The agent may switch in either direction when it improves readability and maintenance.
- `compact`: Use compact layout; switch only when the user requests it.
- `structured`: Use structured layout; switch only when the user requests it.

Judge the **whole goal**, including its complete plan, dependencies, background, design evolution, and accumulated history. Compact fits focused goals with little context and plan history. Structured fits multiple milestones, complex dependencies, or substantial evolving context and history. Remaining task count alone is not a reason to switch; approaching completion does not make a large goal small. Avoid frequent switching with little benefit.

Read existing documents by meaning; headings and wording may differ from the examples. Templates guide organization and should not block recovery of valid user-edited content. Under `auto`, retain `auto` in configuration; the active files identify the actual layout.

## Switching procedure

1. Inspect every goal document and subdirectory. Map all content to the destination layout, preserving goal, acceptance, completion state, stage identifiers, dependencies, reviews, decisions, and all execution and plan-change history.
2. Before edits, copy the full contents of `roadmap/` to a unique `.checkpoint-karpathy/private/work/backups/roadmap-layout/<timestamp>-<source>-to-<target>/` directory. Use this private path in both modes. Put the original files and subdirectories directly in the backup, verify the copy is complete, and do not overwrite a prior backup.
3. Prepare and inspect the target documents, using `private/work/drafts/` if needed. Check destination conflicts. Keep progress history intact; preserve meaning when updating its links. Do not discard custom sections merely because they are absent from a template.
4. Reorganize contents inside the fixed `roadmap/`. Update relative links and anchors; retain stable identifiers. Relocate superseded files individually to a separate subdirectory of the backup rather than leaving conflicting active layouts. Follow project deletion rules.
5. Verify content coverage, completion and phase states, history, links, and the new entry point against the backup. If the conversion fails, preserve the partial result separately and restore the backed-up content before continuing work.
6. Record the reason, source and target layouts, and backup path in the active plan-change log. A layout switch is not a new goal and does not trigger goal archiving. Change configuration only to reflect the user's requested setting.

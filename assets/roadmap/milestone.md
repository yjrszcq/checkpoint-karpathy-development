<a id="milestone-${id}"></a>

## Milestone ${id}: ${title}
Purpose: ${purpose}
Dependencies: ${dependencies}

${phases}

- [ ] Milestone ${id} Review
  - Trigger: After every planned subphase above is complete and committed.
  - Phase label: Phase ${last_phase} Milestone Review
  - Scope: Work introduced or substantially touched by this milestone.
  - Order: Confirm scope, simplify, verify broadly, review, debug and fix, reverify, record, commit.
  - Success criteria: No unresolved in-scope defects, failing checks, or avoidable complexity remain.
  - Verification: ${review_verification}
  - Commit target: ${review_commit}

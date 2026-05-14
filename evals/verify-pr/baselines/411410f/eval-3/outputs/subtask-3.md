## Repository
sdlc-plugins

## Target Branch
main

## Description
Improve the plan-feature skill to recognize when cascade update patterns across multiple database tables require transactional semantics, and include explicit transaction guidance in the generated task's Implementation Notes.

During verification of TC-9103 (SBOM soft-delete endpoint), a reviewer flagged that three UPDATE statements in the `soft_delete` method should be wrapped in a single database transaction. The task's Implementation Notes described the cascade logic ("update sbom_package and sbom_advisory rows") but did not mention transactional wrapping. The plan-feature skill should detect when a task involves mutating multiple related tables and add an Implementation Note about ensuring atomicity via transactions.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — add guidance in the task generation section to check for multi-table mutation patterns and include transaction requirements in Implementation Notes

## Implementation Notes
- In the plan-feature skill's task generation logic, when Implementation Notes describe updates to multiple database tables (e.g., cascade updates, cross-table consistency), add an explicit note about wrapping the operations in a database transaction
- The guidance should be method-level (language-agnostic): "When the task involves mutating multiple related tables, include an Implementation Note requiring transactional wrapping to ensure atomicity"
- This is a method improvement, not a fact insertion — the skill should detect the multi-table mutation pattern and prescribe the transaction requirement

## Acceptance Criteria
- [ ] plan-feature skill documentation includes guidance to detect multi-table mutation patterns
- [ ] When a task involves cascade updates across multiple tables, the generated Implementation Notes include a transaction requirement
- [ ] The guidance is language-agnostic (references "transaction" generically, not a specific ORM API)

## Test Requirements
- [ ] Verify that a task description involving cascade updates across multiple tables includes transaction guidance in Implementation Notes

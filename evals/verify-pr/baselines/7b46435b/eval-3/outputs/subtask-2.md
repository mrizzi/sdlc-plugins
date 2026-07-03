## Repository
sdlc-plugins

## Target Branch
main

## Description
Improve the implement-task skill to verify that multi-table mutation operations are wrapped in database transactions. The TC-9103 verification revealed that a `soft_delete` method writing to three tables (`sbom`, `sbom_package`, `sbom_advisory`) was implemented without transaction wrapping, risking partial updates on failure. This is a method-level skill gap: the knowledge that multi-table writes require transactional atomicity is universal (applies to any repository, any database framework) and can be expressed as a language-agnostic analysis method.

## Files to Modify
- `plugins/sdlc-workflow/skills/implement-task/SKILL.md` -- add a verification step that checks whether multi-table mutation methods use transaction wrapping

## Implementation Notes
- Add guidance in the implement-task skill's code generation or review phase to check: "When a method performs write operations (INSERT, UPDATE, DELETE) on more than one table, verify that all operations are wrapped in a database transaction"
- This is a method-based check (language-agnostic): it applies to any ORM or raw SQL, any language, any framework. The check is "count the number of distinct tables being mutated in a single method; if > 1, verify transaction wrapping"
- Do not embed framework-specific transaction APIs (e.g., SeaORM's `db.transaction()`) in the skill -- those belong in CONVENTIONS.md. The skill should only prescribe the analysis method
- Reference: reviewer feedback on TC-9103 PR #744 identified the missing transaction as a data consistency risk

## Acceptance Criteria
- [ ] implement-task SKILL.md includes guidance to verify transaction wrapping for multi-table mutations
- [ ] The guidance is expressed as a language-agnostic method (not tied to a specific ORM or framework)

## Test Requirements
- [ ] Review the updated SKILL.md guidance for clarity and verify it would have caught the TC-9103 defect

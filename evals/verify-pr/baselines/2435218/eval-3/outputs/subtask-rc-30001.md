## Repository
sdlc-plugins

## Description
Improve the plan-feature skill to detect multi-table cascade operations and include transactional wrapping guidance in task Implementation Notes. When a task involves updating multiple related database tables as part of a single logical operation (e.g., soft-delete cascading to join tables), the plan-feature skill should explicitly note that these operations must be wrapped in a database transaction to ensure atomicity.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance for detecting cascade operations during task planning and including transaction requirements in Implementation Notes

## Implementation Notes
- In the task generation logic, when Implementation Notes describe operations that update multiple tables based on a shared foreign key or relationship, add a note about transactional wrapping
- The guidance should be expressed as a method: "When a task involves multiple related database mutations (cascade updates, multi-table inserts, coordinated deletes), specify in Implementation Notes that these operations must be wrapped in a transaction"
- This is a language-agnostic analysis technique: check whether the planned changes involve multiple related mutations, and if so, note the atomicity requirement
- Do not embed framework-specific transaction APIs (e.g., SeaORM's `transaction()`) in the skill -- those belong in per-project CONVENTIONS.md

## Acceptance Criteria
- [ ] The plan-feature skill includes guidance to detect multi-table cascade operations
- [ ] Task descriptions generated for cascade operations include transactional wrapping notes in Implementation Notes
- [ ] The guidance is expressed as a language-agnostic method, not tied to a specific framework

## Root-Cause Analysis
- **Defect:** The `soft_delete` method updated three tables without transaction wrapping, risking inconsistent state on partial failure
- **Originating phase:** plan-feature -- the task description's Implementation Notes described cascade logic without mentioning transactional atomicity
- **Universality test:** Universal -- "wrap related mutations in a transaction" applies to any database-backed application
- **Method-vs-Fact test:** Method -- "verify multi-table mutations are wrapped in a transaction" is language-agnostic
- **Reference:** Root-cause analysis from TC-9103 verification, review comment 30001

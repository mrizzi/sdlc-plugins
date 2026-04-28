## Repository
sdlc-plugins

## Description
Improve the plan-feature skill to include transactional atomicity guidance when generating Implementation Notes that describe multiple related database operations. Currently, when a task involves cascade updates across multiple tables, the plan-feature skill describes the individual operations but does not specify that they should be wrapped in a database transaction. This leads to implementations that perform related writes independently, risking inconsistent state on partial failure.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance in the task generation instructions to check for multi-table write operations and include transactional atomicity requirements in Implementation Notes when cascade or related updates span multiple tables

## Implementation Notes
- The plan-feature skill generates Implementation Notes for each task. When the skill detects that a task involves updating multiple related database tables (e.g., cascade deletes, cascade updates, multi-entity state transitions), it should include a note specifying that these operations must be wrapped in a transaction
- This is a method-level improvement: "when describing operations that update multiple related tables, specify that atomicity is required" -- it does not prescribe any specific API or framework syntax
- The check should apply universally regardless of the target repository's database framework

## Acceptance Criteria
- [ ] The plan-feature skill includes transactional atomicity guidance in Implementation Notes when generating tasks that involve related updates across multiple database tables
- [ ] The guidance is expressed as a method ("wrap related multi-table updates in a transaction") without prescribing framework-specific syntax

## Test Requirements
- [ ] Verify that a plan-feature run for a cascade-update task includes atomicity guidance in the generated Implementation Notes

## Repository
sdlc-plugins

## Description
Improve the plan-feature skill to include index creation guidance when migrations add columns that will be used in frequent WHERE clauses. When a task adds a column that the implementation will filter on by default (e.g., a soft-delete timestamp filtered with `IS NULL` on every list query), the plan-feature skill should include index requirements in the migration specification.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance for detecting frequently-filtered columns during migration planning and including index requirements

## Implementation Notes
- In the task generation logic, when a migration adds a new column and the same task adds query logic that filters on that column by default, the plan-feature skill should flag this as needing an index
- The guidance should be expressed as a method: "When a task adds a column and also adds queries that filter on that column by default (especially columns where the majority of rows will have NULL/empty values, like soft-delete timestamps), include index creation in the migration requirements"
- This is a language-agnostic analysis technique: correlate new columns with their query patterns to determine if indexes are needed
- Specific index types (partial indexes, composite indexes) are database-specific and belong in per-project CONVENTIONS.md, not in the skill

## Acceptance Criteria
- [ ] The plan-feature skill includes guidance to correlate new columns with their query usage patterns
- [ ] Task descriptions generated for migrations that add frequently-filtered columns include index requirements
- [ ] The guidance is expressed as a language-agnostic method, not tied to a specific database

## Root-Cause Analysis
- **Defect:** The migration added a `deleted_at` column without an index, despite the list endpoint filtering on `deleted_at IS NULL` on every default query
- **Originating phase:** plan-feature -- the task description specified adding the `deleted_at` column but did not mention adding an index for it
- **Universality test:** Universal -- "add indexes for frequently-filtered columns" applies to any SQL database
- **Method-vs-Fact test:** Method (at the detection level) -- "when a task adds a column and filters on it by default, note the need for an index" is language-agnostic; the specific index type (partial index) is a database-specific fact that belongs in CONVENTIONS.md
- **Reference:** Root-cause analysis from TC-9103 verification, review comment 30002

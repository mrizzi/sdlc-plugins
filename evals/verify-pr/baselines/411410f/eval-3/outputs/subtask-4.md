## Repository
trustify-backend

## Target Branch
main

## Description
Document the project's database indexing conventions in CONVENTIONS.md, specifically the requirement to add indexes for columns used in frequent filter conditions (e.g., soft-delete `deleted_at IS NULL` queries). During verification of TC-9103, a reviewer identified that the migration adding a `deleted_at` column lacked a partial index for the frequent `IS NULL` filter. This convention should be documented so that future migrations automatically include appropriate indexes.

## Files to Modify
- `CONVENTIONS.md` — add a section documenting database indexing conventions for migration files

## Implementation Notes
- Add a "Database Indexes" or "Migration Conventions" section to CONVENTIONS.md
- Document the convention: when adding a column that will be used in frequent WHERE clauses (especially soft-delete patterns), include an appropriate index in the same migration
- Include guidance on partial indexes for nullable columns used in IS NULL filters (e.g., `CREATE INDEX idx_<table>_not_deleted ON <table> (deleted_at) WHERE deleted_at IS NULL`)
- Reference existing migration patterns in the codebase for consistency

## Acceptance Criteria
- [ ] CONVENTIONS.md contains a documented convention for adding indexes in migrations when new columns are used in frequent filter conditions
- [ ] The convention includes guidance on partial indexes for soft-delete patterns
- [ ] The convention is discoverable by automated tooling (clear section heading, searchable terms)

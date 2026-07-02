## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create GIN indexes on searchable text columns across SBOM, advisory, and package entities. This addresses the "search should be faster" requirement by enabling PostgreSQL to use index-accelerated full-text search instead of sequential scans.

**Ambiguity note:** The feature specifies "search should be faster" and "currently too slow" without providing baseline metrics or target latency. **Assumption pending clarification:** We assume that adding GIN indexes on tsvector columns for the primary searchable fields (SBOM name/description, advisory title/description, package name) will provide adequate performance improvement. Actual performance gains should be measured before and after deployment.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables for full-text search

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration conventions.

The migration should:
1. Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
2. Create GIN indexes on each `search_vector` column for fast full-text lookups
3. Populate the `search_vector` columns using `to_tsvector('english', ...)` on relevant text fields
4. Add a trigger to keep `search_vector` columns updated on INSERT/UPDATE

For the `sbom` table, the tsvector should cover name-related fields. For `advisory`, it should cover title and description fields. For `package`, it should cover the package name field.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for any fallible operations in the migration. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Migration creates `search_vector` tsvector columns on `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Existing rows have their `search_vector` columns populated
- [ ] Triggers maintain `search_vector` on future INSERT/UPDATE operations
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against an existing database with data

## Test Requirements
- [ ] Migration applies without errors on an empty database
- [ ] Migration applies without errors on a database with existing data
- [ ] Rolling back the migration removes the indexes, triggers, and columns

## Dependencies
- Depends on: None

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira

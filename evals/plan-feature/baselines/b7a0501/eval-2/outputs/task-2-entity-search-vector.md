# Task 2 — Update Entity Definitions for Full-Text Search Column

## Repository
trustify-backend

## Description
Update the SeaORM entity definitions for sbom, advisory, and package to include the new `search_vector` tsvector column added by the migration in Task 1. This ensures the ORM layer is aware of the new column so it can be used in queries by the search service.

## Files to Modify
- `entity/src/sbom.rs` — Add `search_vector` field to the SBOM entity
- `entity/src/advisory.rs` — Add `search_vector` field to the Advisory entity
- `entity/src/package.rs` — Add `search_vector` field to the Package entity

## Implementation Notes
- Follow the existing entity field pattern in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`
- The `search_vector` column should be mapped as an optional field since it is populated by a trigger and should not be set directly by application code in most cases
- SeaORM may require a custom type mapping for PostgreSQL's `tsvector` type — check if SeaORM provides a native `TsVector` type or if a raw SQL type annotation is needed
- Per constraints doc section 5.2: inspect each entity file before modifying to understand the existing field patterns and derive macro usage

## Reuse Candidates
- `entity/src/sbom.rs` — Existing entity definition pattern to follow for adding new fields
- `entity/src/advisory.rs` — Same entity pattern
- `entity/src/package.rs` — Same entity pattern

## Acceptance Criteria
- [ ] `sbom.rs` entity includes `search_vector` field with correct type mapping
- [ ] `advisory.rs` entity includes `search_vector` field with correct type mapping
- [ ] `package.rs` entity includes `search_vector` field with correct type mapping
- [ ] All entity definitions compile without errors
- [ ] Existing queries and operations remain unaffected

## Test Requirements
- [ ] Entity definitions compile and are compatible with the database schema after migration
- [ ] Existing integration tests in `tests/api/sbom.rs` and `tests/api/advisory.rs` continue to pass

## Dependencies
- Depends on: Task 1 — Add Database Migration for Search Indexes and Full-Text Search Support

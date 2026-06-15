# Task 1: Add database migration for full-text search indexes

## Repository

trustify-backend

## Target Branch

main

## Description

Create a database migration that adds PostgreSQL full-text search indexes to support faster and more relevant search queries. The current search implementation lacks dedicated indexes, resulting in sequential scans on text columns. This migration adds GIN indexes on `tsvector` columns for SBOMs, advisories, and packages to enable efficient full-text search with ranking.

**Ambiguity note:** The feature description does not specify which fields should be indexed for search. **Assumption pending clarification:** We index the primary text fields that users would search against: SBOM names/descriptions, advisory titles/descriptions, and package names/versions. These are the fields most likely referenced when users report "irrelevant results."

## Files to Create

- `migration/src/m0002_search_indexes/mod.rs` — New migration module adding GIN indexes for full-text search

## Files to Modify

- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes

- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` — each migration is a submodule under `migration/src/` registered in `lib.rs`.
- Use `CREATE INDEX ... USING GIN (to_tsvector('english', <column>))` for full-text search indexes on text columns in the `sbom`, `advisory`, and `package` tables.
- Add a composite `tsvector` column or expression index that combines multiple text fields per entity (e.g., for advisories: title + description) to support weighted ranking in Task 2.
- The migration framework uses SeaORM — use `sea_orm_migration::prelude::*` and implement the `MigrationTrait` with `up` and `down` methods.
- **Assumption pending clarification:** Index configuration assumes English language stemming (`'english'` text search configuration). If the platform supports multilingual content, this should be revisited.

## Acceptance Criteria

- [ ] Migration creates GIN indexes on text columns for `sbom`, `advisory`, and `package` tables
- [ ] Migration is reversible (`down` method drops the indexes)
- [ ] Migration module is registered in `migration/src/lib.rs`
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Existing data and queries are not broken by the migration

## Test Requirements

- [ ] Migration applies cleanly on a fresh database
- [ ] Migration applies cleanly on a database with existing data
- [ ] Migration rollback (`down`) executes without errors
- [ ] Indexes are visible in `pg_indexes` after migration

## Verification Commands

- `cargo test -p migration` — Run migration tests
- `psql -c "SELECT indexname FROM pg_indexes WHERE tablename IN ('sbom', 'advisory', 'package') AND indexdef LIKE '%gin%';"` — Verify indexes exist

## Dependencies

None — this is the foundational task.

---

[Description digest: sha256-md:a3c1f8e92b4d7605c8e1a9f3b2d4e6a8c0f2d4e6a8b0c2d4e6f8a0b2c4d6e8f0 would be posted as a comment]

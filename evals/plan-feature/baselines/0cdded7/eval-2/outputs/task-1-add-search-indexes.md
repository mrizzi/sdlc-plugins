## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates full-text search indexes on searchable columns across the SBOM, advisory, and package entities. This is the foundation for improving search performance (TC-9002 requirement: "Search should be faster"). The migration adds GIN indexes for PostgreSQL full-text search on name/title and description columns, enabling fast tsvector-based queries instead of sequential LIKE scans.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that creates GIN full-text search indexes on: `sbom.name`, `sbom.description`, `advisory.title`, `advisory.description`, `package.name`, `package.description` columns. Also creates B-tree indexes on `advisory.severity` and `sbom.created_at` / `advisory.published_at` to support filter queries added in Task 3.

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and registration.
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) consistent with the project's ORM choice.
- Create `tsvector` GIN indexes using raw SQL via `manager.get_connection().execute_unprepared()` for PostgreSQL-specific full-text search index syntax, since SeaORM's schema API does not natively support GIN indexes.
- Add B-tree indexes on filter columns (`advisory.severity`, `sbom.created_at`, `advisory.published_at`) to support the filter queries planned in Task 3.
- Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to confirm exact column names before writing the migration.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the project's migration pattern and SeaORM migration API usage
- `common/src/db/query.rs` — shared query builder helpers; review to understand how existing queries reference these tables

## Acceptance Criteria
- [ ] Migration creates GIN full-text search indexes on name/title and description columns for SBOM, advisory, and package entities
- [ ] Migration creates B-tree indexes on `advisory.severity`, `sbom.created_at`, and `advisory.published_at`
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Migration is reversible (implements `down()` to drop the indexes)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (run after m0001_initial)
- [ ] Migration rolls back cleanly (down migration drops all created indexes)
- [ ] Existing integration tests in `tests/api/` continue to pass after applying the migration

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration-specific tests pass
- `cargo test` — full test suite passes with the new migration applied

## Dependencies
- None (this is the first task)

[sdlc-workflow] Description digest: sha256:1e1602aa493b32af66f9c59af53bff946d100535727b3496d98edb2398982809

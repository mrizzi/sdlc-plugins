## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates indexes on commonly searched columns to improve search query performance. This is a foundational task that addresses the "search should be faster" requirement by ensuring the database layer can efficiently execute full-text search queries.

Assumption (pending clarification): Without concrete performance targets from the feature description ("should be fast enough"), this task assumes the goal is to ensure all columns used in full-text search have appropriate GIN/GiST indexes for PostgreSQL text search, and that B-tree indexes exist on commonly filtered columns.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration module adding indexes for search optimization

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
The migration should add the following indexes:

1. A GIN index on SBOM name/description fields used in full-text search (referenced from `entity/src/sbom.rs` entity definition)
2. A GIN index on Advisory title/description fields (referenced from `entity/src/advisory.rs` entity definition)
3. A GIN index on Package name fields (referenced from `entity/src/package.rs` entity definition)
4. B-tree indexes on `advisory.severity` (referenced from `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary includes severity field) and `package_license.license` for filter support in later tasks

Assumption (pending clarification): The exact column names for text search are assumed based on typical SBOM/advisory domain models. The actual column names should be verified against the SeaORM entity definitions in `entity/src/`.

In `migration/src/lib.rs`, add the new migration to the migrator's list of migrations following the existing pattern established by `m0001_initial/`.

Per CONVENTIONS.md §Module pattern: Follow existing migration structure as established in `migration/src/m0001_initial/mod.rs`.
Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the migration module convention.

## Acceptance Criteria
- [ ] Migration creates GIN indexes for full-text search on SBOM, advisory, and package text columns
- [ ] Migration creates B-tree indexes on severity and license columns for filter support
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Migration is reversible (implements down/rollback)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration rolls back cleanly
- [ ] Existing search queries continue to work after migration (note: based on assumption that indexes are additive and non-breaking, pending clarification on backward compatibility requirements)

[sdlc-workflow] Description digest: sha256-md:65c56cac6124393247bff305b13b407a2e09286afcd2c266722ac8be549bb74e

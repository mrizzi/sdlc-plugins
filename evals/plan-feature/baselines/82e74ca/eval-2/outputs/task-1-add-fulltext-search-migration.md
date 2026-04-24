# Task 1 — Add Full-Text Search Migration

## Repository
trustify-backend

## Description
Create a database migration that adds PostgreSQL full-text search infrastructure to support faster and more relevant search results. This includes adding `tsvector` columns to the searchable entities (SBOM, advisory, package) and creating GIN indexes on those columns. This is the foundational task that enables all subsequent search improvements.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_fulltext_search/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- Use SeaORM migration traits (`MigrationTrait`, `SchemaManager`) consistent with the existing migration infrastructure.
- Add `tsvector` columns to the following tables:
  - `sbom` — generated from the `name` column (weight A) and any description fields (weight B)
  - `advisory` — generated from the `title` column (weight A) and `description` column (weight B)
  - `package` — generated from the `name` column (weight A)
- Create GIN indexes on each `tsvector` column for efficient full-text search.
- Add a trigger function to keep `tsvector` columns updated when source columns change.
- Per constraints doc 2.1: commit must reference TC-9002 in the footer.
- Per constraints doc 5.2: inspect existing migration code before modifying.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for structure, naming, and SeaORM trait usage

## Acceptance Criteria
- [ ] Migration creates `tsvector` columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all `tsvector` columns
- [ ] Trigger functions keep `tsvector` columns in sync with source columns
- [ ] Migration runs successfully against a clean database
- [ ] Migration is reversible (down migration drops the columns and indexes)

## Test Requirements
- [ ] Migration applies successfully on a fresh database
- [ ] Migration rolls back cleanly
- [ ] tsvector columns are populated correctly after migration on existing data

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors

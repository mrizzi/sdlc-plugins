# Task 2: Update Entities with Search Vector Columns

## Repository
trustify-backend

## Target Branch
main

## Description
Update the SeaORM entity definitions for SBOM, Advisory, and Package to include the new `search_vector` column added by the migration in Task 1. This ensures the ORM layer is aware of the full-text search column so it can be used in queries by the search service.

**Ambiguity note:** The feature description does not clarify whether search vectors should be exposed in API responses. This task assumes the `search_vector` column is internal to the database and should NOT be serialized in API responses (pending clarification).

## Files to Modify
- `entity/src/sbom.rs` — Add `search_vector` field to the SBOM SeaORM entity model
- `entity/src/advisory.rs` — Add `search_vector` field to the Advisory SeaORM entity model
- `entity/src/package.rs` — Add `search_vector` field to the Package SeaORM entity model

## Implementation Notes
- Each entity file defines a SeaORM `Model` struct and corresponding `Column` enum. Add a `search_vector` field of an appropriate type. SeaORM does not have a native `tsvector` type, so use a custom column type or `String` with a `#[sea_orm(column_type = "Custom(\"tsvector\".to_string())")]` attribute.
- Ensure the `search_vector` field is excluded from serialization by adding `#[serde(skip_serializing)]` so it does not leak into API responses.
- Follow the existing patterns in `entity/src/sbom.rs` for how entity fields are declared.
- Per CONVENTIONS.md: use SeaORM entity patterns.
  Applies: task modifies `entity/src/sbom.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — Reference existing entity field patterns for column type declarations
- `entity/src/advisory.rs` — Reference for `severity` field type handling (enum/string mapping)

## Acceptance Criteria
- [ ] SBOM entity includes `search_vector` column mapping
- [ ] Advisory entity includes `search_vector` column mapping
- [ ] Package entity includes `search_vector` column mapping
- [ ] `search_vector` field is not serialized in JSON responses (skipped via serde)
- [ ] Project compiles without errors after entity changes

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom.rs` and `tests/api/advisory.rs` continue to pass (regression check)
- [ ] Entity round-trip test: insert a record with `search_vector` populated and read it back

## Dependencies
- Depends on: Task 1 — Add database migration for full-text search indexes

---

`[sdlc-workflow] Description digest: sha256-md:b7d29a4e6f183c5d0a92e7b4c6d8f15a3e7b90c2d4f6a8e1c3b5d7f9a0c2e4b6`

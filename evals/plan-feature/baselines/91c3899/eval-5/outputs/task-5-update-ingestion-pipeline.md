# Task 5 — Update advisory ingestion pipeline for status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting a row into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline must map incoming status strings from advisory feeds to the corresponding `AdvisoryStatusEnum` variant.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Update advisory ingestion logic to set the `status` field using `AdvisoryStatusEnum` instead of looking up/inserting into the `advisory_status` table; remove any `advisory_status` table inserts or lookups
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references `advisory_status` during ingestion orchestration

## Implementation Notes
- The current ingestion flow in `graph/advisory/mod.rs` likely: (1) looks up or inserts the status string in `advisory_status`, (2) gets the `id`, (3) sets `status_id` on the advisory row. Replace this with: (1) parse the status string to `AdvisoryStatusEnum` variant, (2) set `status` directly on the advisory active model
- Use a match expression or `FromStr`/`TryFrom` implementation on `AdvisoryStatusEnum` to map incoming status strings (e.g., `"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`) to enum variants. Handle invalid status strings with a descriptive error using `AppError` with `.context()`
- Remove any `use` imports of `advisory_status` entity from the ingestor module
- Check `modules/ingestor/src/graph/sbom/mod.rs` for a sibling ingestion pattern to follow for consistency
- Per docs/constraints.md §5.2: inspect existing ingestion code before modifying
- Per docs/constraints.md §5.4: reuse the `AdvisoryStatusEnum` type defined in Task 3 rather than duplicating enum definitions
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type created in Task 3; use this directly for status mapping in the ingestion pipeline
- `modules/ingestor/src/graph/sbom/mod.rs` — Sibling ingestion module demonstrating the project's ingestion pattern (parse, store, link)
- `common/src/error.rs::AppError` — Error handling enum for wrapping ingestion errors

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` value directly to `advisory.status` column
- [ ] No references to `advisory_status` table remain in the ingestor module
- [ ] Invalid status strings during ingestion produce a descriptive error
- [ ] Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) works correctly

## Test Requirements
- [ ] Ingesting an advisory with status "New" stores `AdvisoryStatusEnum::New` in the database
- [ ] Ingesting an advisory with status "Fixed" stores `AdvisoryStatusEnum::Fixed` in the database
- [ ] Ingesting an advisory with an invalid status string returns an appropriate error
- [ ] Existing ingestion tests continue to pass after refactor

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles cleanly
- `cargo test -p ingestor` — ingestor unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

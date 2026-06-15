## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of inserting into the `advisory_status` lookup table first. The pipeline currently writes a status row to the lookup table and then references it via foreign key. After this change, the pipeline maps the status string from the advisory feed directly to an `AdvisoryStatusEnum` value and inserts it into the `status` column on the `advisory` row.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove the lookup table insert for advisory status; map the status string from the parsed advisory to an `AdvisoryStatusEnum` value; set the `status` field directly on the advisory `ActiveModel` during insertion
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references advisory status lookup table operations or types

## Implementation Notes
Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how entities are constructed and inserted.

The status string mapping should handle the four known values: `"New"` -> `AdvisoryStatusEnum::New`, `"Analyzing"` -> `AdvisoryStatusEnum::Analyzing`, `"Fixed"` -> `AdvisoryStatusEnum::Fixed`, `"Rejected"` -> `AdvisoryStatusEnum::Rejected`. Use a `match` expression with an error case for unrecognized values, following the error handling pattern with `AppError` and `.context()` from `common/src/error.rs`.

Import `AdvisoryStatusEnum` from the entity crate (`entity::advisory::AdvisoryStatusEnum`).

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — existing ingestion implementation showing entity construction and insertion patterns
- `common/src/error.rs` — `AppError` enum for error handling in the ingestion pipeline

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly to the `advisory` table
- [ ] No references to `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Unrecognized status strings produce a descriptive error
- [ ] The ingestion module compiles without errors

## Test Requirements
- [ ] Ingestion of an advisory with status "Fixed" writes `AdvisoryStatusEnum::Fixed` to the `status` column
- [ ] Ingestion of an advisory with status "New" writes `AdvisoryStatusEnum::New` to the `status` column
- [ ] Ingestion of an advisory with an unrecognized status produces an appropriate error

## Verification Commands
- `cargo check -p ingestor` — module compiles cleanly
- `cargo test -p ingestor` — existing ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:e89aa42195f2b6cca355a9fb3df0a026d0db14f3fc52466643dd0f537fe69c38

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline should map incoming status strings to `AdvisoryStatusEnum` values during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace lookup table insertion logic with direct enum value assignment; map incoming advisory status strings to `AdvisoryStatusEnum` variants; remove any references to the `advisory_status` entity or table
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references `advisory_status` for status resolution or validation
- `modules/ingestor/src/lib.rs` — Remove any `advisory_status` entity imports

## Implementation Notes
Follow the existing advisory ingestion pattern in `modules/ingestor/src/graph/advisory/mod.rs`. The current code likely inserts a row into `advisory_status` (or looks up an existing row) and then sets `advisory.status_id` to the resulting ID. Replace this with:

1. Parse the incoming status string from the advisory feed
2. Map it to an `AdvisoryStatusEnum` variant (New, Analyzing, Fixed, Rejected)
3. Set the `status` field directly on the advisory `ActiveModel`

Use a match expression or `FromStr` implementation on `AdvisoryStatusEnum` for the mapping. Handle unknown status values with an appropriate error using the `AppError` pattern from `common/src/error.rs` with `.context()` wrapping.

Import `AdvisoryStatusEnum` from the entity crate (`entity::advisory::AdvisoryStatusEnum`).

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to the `status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] Unknown status strings during ingestion produce a descriptive error
- [ ] Successfully ingested advisories have the correct enum status value

## Test Requirements
- [ ] Add a test for advisory ingestion that verifies the enum status is written correctly for each status value (New, Analyzing, Fixed, Rejected)
- [ ] Add a test for advisory ingestion with an unknown status string that verifies an error is returned
- [ ] Verify round-trip: ingest an advisory, then query it via the API and confirm the status matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 3 — Update SeaORM entity definitions

[sdlc-workflow] Description digest: sha256-md:92a744e4bb91a07fac11d96fd51e76d51af7f8daddb3962505d77f6ee34954eb

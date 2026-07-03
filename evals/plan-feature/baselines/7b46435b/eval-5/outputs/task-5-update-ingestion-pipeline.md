## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the advisory.status column instead of inserting rows into the advisory_status lookup table and referencing them via foreign key. The pipeline must map incoming status strings from advisory feeds to AdvisoryStatus enum values and set them directly on the advisory record during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace advisory_status table insert + FK assignment with direct enum column write; map status strings to AdvisoryStatus enum values
- `modules/ingestor/src/service/mod.rs` — update IngestorService if it references advisory_status table operations or status_id assignments

## Implementation Notes
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how entities are constructed and persisted during ingestion
- Map incoming status strings to the `AdvisoryStatus` enum defined in `entity/src/advisory.rs` — use a match expression or `FromStr` implementation
- Remove any logic that inserts into or reads from the advisory_status lookup table
- Handle invalid or missing status values by defaulting to `AdvisoryStatus::New` or returning an error, following the error handling pattern in `common/src/error.rs`

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — existing ingestion pattern demonstrating entity construction and persistence during ingestion
- `common/src/error.rs` — AppError enum for error handling

## Acceptance Criteria
- [ ] Ingestion pipeline writes AdvisoryStatus enum values directly to the advisory.status column
- [ ] No remaining writes to or reads from the advisory_status table in the ingestor module
- [ ] Status string mapping covers all four values: New, Analyzing, Fixed, Rejected
- [ ] Invalid status strings are handled gracefully (default or error)
- [ ] Ingestor module compiles without errors

## Test Requirements
- [ ] Ingestion of an advisory with each valid status value produces the correct enum value in the database
- [ ] Ingestion with an invalid status string is handled without panic

## Verification Commands
- `cargo build -p trustify-ingestor` — ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 3 — Update SeaORM entity definitions (ingestion uses the updated advisory entity with enum status)

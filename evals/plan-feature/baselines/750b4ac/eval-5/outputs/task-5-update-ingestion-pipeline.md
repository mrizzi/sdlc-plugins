# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `status` column on the `advisory` table, instead of inserting into the `advisory_status` lookup table and referencing via foreign key. The ingestion pipeline currently writes a status row to `advisory_status` first, then uses the generated ID as `status_id` on the advisory insert. After this change, the pipeline maps the incoming status string to the `AdvisoryStatusEnum` variant and sets the `status` field directly on the advisory insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove logic that inserts into `advisory_status` table and retrieves the `status_id`; replace with direct mapping of status string to `AdvisoryStatusEnum` variant; set `status` field on advisory `ActiveModel` insert
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity or uses the lookup table for status resolution

## Implementation Notes
- The advisory ingestion in `modules/ingestor/src/graph/advisory/mod.rs` currently parses advisory feeds, looks up or creates a status row in `advisory_status`, and uses the returned ID as `status_id`. Replace this with a direct string-to-enum mapping: parse the status string from the feed and convert to `AdvisoryStatusEnum::New`, `AdvisoryStatusEnum::Analyzing`, etc.
- Handle invalid status strings gracefully — if the feed contains an unrecognized status value, return an `AppError` with context rather than silently dropping or panicking. Follow the error handling pattern in `common/src/error.rs`.
- Remove any imports of the `advisory_status` entity from the ingestor module.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for consistent error handling and entity insertion patterns.
- Per docs/constraints.md section 5.2: inspect the ingestion code before modifying to understand the current status insertion flow.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern showing entity insertion without lookup table indirection
- `common/src/error.rs` — `AppError` enum for consistent error handling when status string mapping fails

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No references to `advisory_status` entity or table remain in the ingestor module
- [ ] Invalid status strings produce a clear error rather than panicking
- [ ] Advisory ingestion produces identical results as before (same advisories with same status values)

## Test Requirements
- [ ] Ingestion of advisory with status "New" correctly sets `status = AdvisoryStatusEnum::New`
- [ ] Ingestion of advisory with status "Fixed" correctly sets `status = AdvisoryStatusEnum::Fixed`
- [ ] Ingestion with invalid status string returns descriptive error

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles
- `cargo test -p ingestor` — ingestor tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:c7a6c4cf18fd6e3f81b04232e3dc165a4fc55b7e839afd347045d3f68ff65c69

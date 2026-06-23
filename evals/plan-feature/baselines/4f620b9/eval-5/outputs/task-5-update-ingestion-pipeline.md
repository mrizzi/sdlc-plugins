# Task 5 — Update advisory ingestion pipeline to write enum status directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of inserting a row into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently maps incoming advisory status strings to lookup table rows; it must now map them directly to the enum type.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace advisory status lookup table insertion with direct enum value assignment; update the advisory insert/update logic to set the `status` column to the appropriate `AdvisoryStatusEnum` variant
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references advisory status lookup table operations

## Implementation Notes
- The ingestion pipeline currently parses an advisory status string from the feed, looks up or inserts a row in `advisory_status`, then uses the resulting ID as `status_id` on the advisory row. Replace this with: parse the status string, convert to `AdvisoryStatusEnum` variant, set `advisory.status` directly.
- Use a match statement or `FromStr` impl on `AdvisoryStatusEnum` to convert the incoming status string: `"New" => AdvisoryStatusEnum::New`, etc.
- Handle unknown status values gracefully — if the feed contains a status not in the enum, return an `AppError` with a descriptive message rather than panicking.
- The SBOM ingestion in `modules/ingestor/src/graph/sbom/mod.rs` is a good reference for ingestion patterns that write directly to entity columns without lookup tables.
- Per docs/constraints.md §5 (Code Change Rules): inspect the ingestion code before modifying; follow existing patterns in the ingestor module.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference ingestion implementation demonstrating direct entity column writes without lookup table indirection
- `common/src/error.rs` — `AppError` for error handling on invalid status values

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Unknown status values produce a clear error instead of a panic
- [ ] Ingestion of advisories with all four valid statuses (New, Analyzing, Fixed, Rejected) works correctly

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status (New, Analyzing, Fixed, Rejected) writes the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status produces an appropriate error
- [ ] Verify compilation: `cargo check -p ingestor`

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles cleanly
- `cargo test -p ingestor` — existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:feac2aeecaa43579c63be358684b3ff275d3de18127d8ec582f9b6590f72d5ff

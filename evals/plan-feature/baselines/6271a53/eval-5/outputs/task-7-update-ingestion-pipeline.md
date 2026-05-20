## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of inserting into the `advisory_status` lookup table and creating a foreign key reference. The pipeline should map status strings from the advisory feed to `AdvisoryStatusEnum` values and set them directly on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Update advisory ingestion logic to map incoming status strings to `AdvisoryStatusEnum` values and insert them directly as the `status` column value; remove any code that inserts into or looks up from the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it has any status-related lookup or resolution logic that references the old table

## Implementation Notes
- The advisory ingestion code in `modules/ingestor/src/graph/advisory/mod.rs` likely has logic that: (1) checks if a status exists in the `advisory_status` table, (2) inserts the status if missing, (3) uses the returned ID as `status_id` on the advisory row. Replace all of this with a direct enum mapping
- Map incoming status strings to `AdvisoryStatusEnum` variants. Handle case sensitivity: the feed may provide "new", "NEW", or "New" -- normalize to match the enum variants
- For unknown or unmappable status values, use a sensible default (e.g., `AdvisoryStatusEnum::New`) or return an error depending on the existing error handling strategy in the ingestion pipeline
- Follow the patterns in `modules/ingestor/src/graph/sbom/mod.rs` for ingestion code structure and error handling
- The ingestion pipeline must remain idempotent -- re-ingesting the same advisory should update the status without errors

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- Reference for ingestion pipeline patterns and error handling
- `entity/src/advisory.rs` -- The `AdvisoryStatusEnum` definition to import for status mapping

## Acceptance Criteria
- [ ] Advisory ingestion writes enum status values directly to the `status` column
- [ ] No code references the `advisory_status` lookup table in the ingestion pipeline
- [ ] Status string mapping handles case-insensitive input
- [ ] Unknown status values are handled gracefully (error or default, matching existing patterns)
- [ ] Ingestion remains idempotent for re-processed advisories
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify advisory ingestion with status "New" writes the correct enum value
- [ ] Verify advisory ingestion with status "Fixed" writes the correct enum value
- [ ] Verify advisory re-ingestion updates the status without errors
- [ ] Verify handling of unexpected status strings (error or default behavior)

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

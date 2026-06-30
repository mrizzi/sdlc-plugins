# Task 6 — Update advisory ingestion pipeline to write enum status directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly into the `advisory` table instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline should map incoming status strings from advisory feeds to `AdvisoryStatusEnum` values and set the enum column on insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove logic that inserts into or looks up the `advisory_status` table; replace with direct enum value assignment when creating advisory records; update the status string-to-enum mapping
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains any references to the advisory status lookup table or intermediary status insertion logic

## Implementation Notes
- The current ingestion flow likely follows this pattern:
  1. Parse advisory from feed, extract status string
  2. Look up or insert the status in `advisory_status` table to get an ID
  3. Insert advisory row with `status_id` referencing the lookup table
- Replace with:
  1. Parse advisory from feed, extract status string
  2. Map status string to `AdvisoryStatusEnum` variant (New, Analyzing, Fixed, Rejected)
  3. Insert advisory row with `status` enum value directly
- For the string-to-enum mapping, use a match statement or `FromStr` implementation. Handle unrecognized status strings by defaulting to `AdvisoryStatusEnum::New` with a warning log, or returning an ingestion error — follow whichever error handling pattern the existing ingestion pipeline uses for invalid data.
- Look at `modules/ingestor/src/graph/sbom/mod.rs` for the established ingestion pattern in this codebase (parse, store, link).
- Remove any imports of the `advisory_status` entity from the ingestor module.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference implementation for the ingestion pattern (parse, store, link packages); follow the same error handling and transaction approach
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3; use this for the status field assignment

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly to the `advisory` table
- [ ] No references to `advisory_status` table remain in the ingestor module
- [ ] Valid status strings from advisory feeds are correctly mapped to enum variants
- [ ] Invalid or unrecognized status strings are handled gracefully (error or default, consistent with existing error handling patterns)
- [ ] Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) works correctly

## Test Requirements
- [ ] Test ingestion of an advisory with status "Fixed" — verify the advisory record has `status = Fixed` enum value
- [ ] Test ingestion of an advisory with each of the four valid status values
- [ ] Test ingestion behavior when an unrecognized status string is provided

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles
- `cargo test -p ingestor -- advisory` — advisory ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

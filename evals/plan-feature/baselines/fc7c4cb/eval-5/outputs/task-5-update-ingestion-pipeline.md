# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and using the resulting ID as a foreign key. This simplifies the ingestion flow by removing the intermediate lookup table write.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert logic with direct enum value assignment; map status strings from the advisory feed to `AdvisoryStatusEnum` variants; remove any references to the `advisory_status` entity or table
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references advisory status lookup table operations or passes status IDs

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, the current ingestion flow likely:
  1. Parses status string from the advisory feed
  2. Looks up or inserts into `advisory_status` table to get the status ID
  3. Inserts the advisory row with `status_id` FK
  
  Replace this with:
  1. Parse status string from the advisory feed
  2. Map the string to an `AdvisoryStatusEnum` variant (e.g., `"Fixed"` -> `AdvisoryStatusEnum::Fixed`)
  3. Insert the advisory row with `status: AdvisoryStatusEnum::Fixed` directly
- Add validation/error handling for unrecognized status strings during ingestion — if the feed contains a status value that does not map to one of the four enum variants, the ingestion should produce a clear error rather than silently failing.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for SeaORM `ActiveModel` insertion patterns.
- Remove `use` imports of `advisory_status` entity from all modified files.
- Use the `AdvisoryStatusEnum` type from `entity/src/advisory.rs` (updated in Task 3) for the enum mapping.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for SeaORM ActiveModel insertion pattern during ingestion
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type to use for mapping status strings

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to `advisory.status` column — no interaction with `advisory_status` table
- [ ] Status string mapping handles all four values: New, Analyzing, Fixed, Rejected
- [ ] Unrecognized status strings produce a clear error during ingestion
- [ ] No references to `advisory_status` entity remain in the ingestor module
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status value (New, Analyzing, Fixed, Rejected) results in the correct enum value stored in the database
- [ ] Verify ingestion with an unrecognized status string produces an appropriate error
- [ ] Verify end-to-end ingestion: ingest advisory, then query via service and confirm the status field is correct

## Verification Commands
- `cargo check -p ingestor` — compiles without errors
- `cargo test -p ingestor -- advisory` — advisory ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256:0ebcd634048f892b0dc32e3891a8ef698e4babbb0306febb612a6eca288b1595

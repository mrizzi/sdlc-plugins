## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the enum status value directly to the `status` column on the `advisory` table, instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline should map the status string from the advisory feed to the `AdvisoryStatusEnum` variant and set it directly on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insertion logic with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any references to `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains any advisory status handling that references the lookup table

## Implementation Notes
- The ingestion pipeline currently writes to the `advisory_status` lookup table first, then references the inserted row via `status_id` FK when creating the advisory row. Replace this two-step process with a single step: map the status string to `AdvisoryStatusEnum` and set it directly on the advisory `ActiveModel`.
- Add validation for the incoming status string — if the feed provides a status value that does not map to one of the four enum variants (New, Analyzing, Fixed, Rejected), the pipeline should return an error rather than silently dropping the status or defaulting.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for reference on how the SBOM ingestion pipeline handles entity creation.
- Remove any `use entity::advisory_status` imports from the ingestor module.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern for reference on entity creation during ingestion
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that should be used for mapping

## Acceptance Criteria
- [ ] Ingestion pipeline maps advisory status strings directly to `AdvisoryStatusEnum` variants
- [ ] Ingestion pipeline writes the enum value directly to the `status` column — no lookup table interaction
- [ ] Invalid status strings are rejected with a clear error message
- [ ] No references to `advisory_status` entity remain in the ingestor module
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status value (New, Analyzing, Fixed, Rejected) produces the correct enum value in the database
- [ ] Verify ingestion with an invalid status string returns an appropriate error

## Verification Commands
- `cargo check -p ingestor` — compiles without errors
- `cargo test -p ingestor` — all ingestor tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions

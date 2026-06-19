## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing by foreign key. The pipeline must map incoming status strings from advisory feeds to `AdvisoryStatusEnum` variants and set the enum value on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace the lookup-table-based status assignment (insert into `advisory_status`, get ID, set `status_id`) with direct enum assignment: parse the status string to `AdvisoryStatusEnum`, set `advisory.status` on the active model
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it coordinates status resolution or references `advisory_status` entity

## Implementation Notes
Follow the existing advisory ingestion pattern in `modules/ingestor/src/graph/advisory/mod.rs`. The current flow likely:
1. Parses the advisory status string from the feed
2. Looks up or inserts the status in the `advisory_status` table
3. Sets `status_id` on the advisory active model

Replace this with:
1. Parse the advisory status string from the feed
2. Map to `AdvisoryStatusEnum` variant (e.g., `"New"` -> `AdvisoryStatusEnum::New`)
3. Set `status` directly on the advisory active model

Handle unknown status values by falling back to a default (e.g., `AdvisoryStatusEnum::New`) or returning an error, following whatever pattern the existing ingestion code uses for invalid data.

Import `AdvisoryStatusEnum` from the entity crate. Remove any imports of `advisory_status` entity.

Follow the sibling ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for general ingestion structure.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion logic to modify in-place
- `modules/ingestor/src/graph/sbom/mod.rs` — Sibling ingestion module for pattern reference
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type to use for direct status assignment

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` value directly to `advisory.status`
- [ ] No insertion into `advisory_status` lookup table during ingestion
- [ ] Status string from feed is correctly mapped to enum variant
- [ ] Unknown or invalid status strings are handled gracefully (error or default)
- [ ] No remaining references to `advisory_status` entity in the ingestor module
- [ ] Ingestor module compiles successfully

## Test Requirements
- [ ] Ingesting an advisory with status "New" sets `advisory.status` to `AdvisoryStatusEnum::New`
- [ ] Ingesting an advisory with status "Fixed" sets `advisory.status` to `AdvisoryStatusEnum::Fixed`
- [ ] Ingesting an advisory with an unknown status value is handled without panic
- [ ] End-to-end ingestion produces an advisory row with correct enum status

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

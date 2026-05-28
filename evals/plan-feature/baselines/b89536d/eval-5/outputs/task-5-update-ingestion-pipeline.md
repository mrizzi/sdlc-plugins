## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently parses the advisory feed, looks up or creates a row in the `advisory_status` table, and sets the `status_id` FK. After this change, it will map the status string from the feed directly to an `AdvisoryStatusEnum` variant and set the `status` column on the advisory row.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Remove all interactions with the `advisory_status` table (lookups, inserts); map the status string from the advisory feed to an `AdvisoryStatusEnum` variant; set the `status` field directly on the advisory `ActiveModel` when inserting or updating advisories
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it contains any references to the `advisory_status` table or `status_id` field

## Implementation Notes
- The feed status strings (New, Analyzing, Fixed, Rejected) must be mapped to `AdvisoryStatusEnum` variants. Use a `match` or `FromStr` implementation to parse the string into the enum. Handle unknown status values with an appropriate error (e.g., return an `AppError` with context rather than silently defaulting).
- Remove any `use entity::advisory_status` imports and any code that queries or inserts into the `advisory_status` table.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how the SBOM ingestion pipeline structures its insert logic — use the same error handling and transaction patterns.
- The ingestion pipeline should continue to use the same transaction boundaries as before — the only change is what gets written (enum value instead of FK reference).

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module showing the established pattern for parsing, storing, and linking entities during ingestion
- `entity/src/advisory.rs` — The updated advisory entity (from Task 3) with the `AdvisoryStatusEnum` type definition

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly to the `advisory` table
- [ ] No code in the ingestor module references the `advisory_status` table or `status_id` field
- [ ] Unknown status values in the feed produce a clear error rather than a silent default
- [ ] Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) succeeds

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" sets the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" sets the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status value produces an error
- [ ] Verify end-to-end ingestion pipeline works with the new schema

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions

# Task 5 -- Update advisory ingestion pipeline to write enum status directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline must map incoming status strings from advisory feeds to the `AdvisoryStatusEnum` variants and insert them directly during advisory ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- update advisory ingestion logic to: (1) map the status string from the feed to an `AdvisoryStatusEnum` variant, (2) set the `status` field on the advisory `ActiveModel` directly instead of creating a lookup table row and storing a `status_id` foreign key; remove any code that inserts into or queries the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references the `advisory_status` entity or `status_id` field in any helper methods or validation logic

## Implementation Notes
- The ingestion pipeline currently likely does something like: look up or insert a row in `advisory_status`, get the `id`, and set `advisory.status_id = id`. Replace this with: parse the status string, convert to `AdvisoryStatusEnum` variant, and set `advisory.status = variant`
- Use a `match` or `FromStr` implementation on `AdvisoryStatusEnum` to map feed status strings to enum variants. Handle unknown status strings with an error rather than silently ignoring them
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for parse-store-link flow structure
- Import `AdvisoryStatusEnum` from the entity crate: `use entity::advisory_status_enum::AdvisoryStatusEnum`
- Remove any `use entity::advisory_status` imports from ingestion code
- Per docs/constraints.md SS2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005
- Per docs/constraints.md SS5.4 (Code Change Rules): do not duplicate status mapping logic if it already exists elsewhere -- reuse the enum's `FromStr` or `TryFrom` implementation

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference for ingestion pipeline structure (parse, store, link pattern)
- `entity/src/advisory_status_enum.rs` -- the enum definition (created in Task 3) provides the mapping variants

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No code in the ingestor module references `advisory_status` entity or `status_id` field
- [ ] Unknown status strings in advisory feeds produce a clear error
- [ ] Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) succeeds

## Test Requirements
- [ ] Test ingestion of an advisory with each valid status value and verify the correct enum is stored
- [ ] Test ingestion of an advisory with an invalid/unknown status value and verify it produces an error
- [ ] Verify that no rows are written to the `advisory_status` table during ingestion (table should not exist post-migration)

## Verification Commands
- `cargo build -p ingestor` -- compiles without errors
- `cargo test -p ingestor` -- all ingestion tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256:8858f90da309874576cd18c6a414f13aaf90410dc0d9af0bea4a2e52397faafe

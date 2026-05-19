# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting rows into the `advisory_status` lookup table and using the resulting ID as a foreign key. The pipeline currently writes to the lookup table first and then references the lookup row's ID when inserting the advisory. After this change, the pipeline maps the status string from the advisory feed directly to an `AdvisoryStatusEnum` variant and inserts it as the `status` column value.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Remove logic that inserts into or queries the `advisory_status` lookup table; replace with direct mapping from feed status string to `AdvisoryStatusEnum` variant; update advisory insert/update to use the `status` enum column instead of `status_id`
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references `advisory_status` entity or `status_id` in advisory ingestion orchestration

## Implementation Notes
- The advisory feed provides status as a string (e.g., "New", "Analyzing", "Fixed", "Rejected"). Map these to `AdvisoryStatusEnum` variants using a `match` or `FromStr` implementation
- Import the `AdvisoryStatusEnum` from the entity crate (`entity::advisory::AdvisoryStatusEnum`)
- Remove any `use` imports of `advisory_status` entity types from the ingestor module
- Handle unknown/invalid status strings gracefully — either reject the advisory with an error or default to a sensible value (e.g., `AdvisoryStatusEnum::New`) with a warning log
- Follow the existing ingestion patterns in `modules/ingestor/src/graph/sbom/mod.rs` for reference on how the SBOM ingestion pipeline handles entity creation
- Per docs/constraints.md: inspect existing code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality
- Per docs/constraints.md: commits must reference Jira issue ID, follow Conventional Commits, and include AI attribution trailer
- Per docs/constraints.md: PR must specify `--base TC-9005`

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline for reference on entity creation patterns without lookup table indirection
- `modules/ingestor/src/graph/advisory/mod.rs` — Existing advisory ingestion logic to be refactored in place
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type defined in Task 3 that this task will import and use

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] No references to `status_id` column remain in the ingestor module
- [ ] Invalid status strings in the feed are handled gracefully (error or default with warning)
- [ ] Ingestion pipeline compiles and functions correctly with the new entity definitions

## Test Requirements
- [ ] Verify advisory ingestion correctly maps each known status string to the corresponding enum variant
- [ ] Verify advisory ingestion handles an unknown status string gracefully
- [ ] Verify ingested advisories have the correct `status` enum value in the database

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

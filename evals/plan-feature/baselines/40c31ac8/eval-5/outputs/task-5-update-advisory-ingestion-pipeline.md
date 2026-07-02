## Summary
Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `AdvisoryStatusEnum` value directly to the `advisory.status` column instead of first inserting a row into the `advisory_status` lookup table and then referencing it via `status_id`. The ingestion pipeline currently maps status strings from advisory feeds to lookup table rows; this must be changed to map them directly to the Rust `AdvisoryStatusEnum` variants.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Update advisory ingestion logic to set `status` enum value directly instead of looking up/inserting into `advisory_status` table; remove any `advisory_status` table interactions
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it references `advisory_status` types or performs status lookups

## Implementation Notes
Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all fallible operations during ingestion. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` scope.

Key changes in `modules/ingestor/src/graph/advisory/mod.rs`:
- Replace any `advisory_status::ActiveModel` inserts with direct `AdvisoryStatusEnum` value assignment
- Map incoming status strings to `AdvisoryStatusEnum` variants (e.g., `"new"` -> `AdvisoryStatusEnum::New`)
- Remove imports of the `advisory_status` entity
- Use the `AdvisoryStatusEnum` from `entity/src/advisory_status_enum.rs`

The mapping should handle case-insensitive matching and return `AppError` for unrecognized status strings.

## Acceptance Criteria
- [ ] Ingestion writes `AdvisoryStatusEnum` value directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unrecognized status strings produce a clear error with context
- [ ] Ingested advisories are queryable by the service layer using the new enum column

## Test Requirements
- [ ] Ingestion of advisory with each valid status value succeeds and stores correct enum
- [ ] Ingestion with unrecognized status string returns appropriate error
- [ ] End-to-end: ingest advisory, then fetch via service layer and verify status field

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira

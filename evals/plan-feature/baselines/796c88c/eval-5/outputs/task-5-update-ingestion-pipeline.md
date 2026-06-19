## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently resolves the status string to a lookup table row ID before inserting the advisory; it must now map the status string directly to the `AdvisoryStatusEnum` Rust enum variant.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Replace lookup-table-based status resolution with direct enum mapping; update the advisory insert/update to set `status: AdvisoryStatusEnum` instead of `status_id`
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it contains status resolution logic or passes status_id to the graph layer

## Implementation Notes
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/advisory/mod.rs` for advisory record creation
- The current flow likely does: parse status string -> find or insert into `advisory_status` table -> use the returned ID as `status_id`. Replace with: parse status string -> map to `AdvisoryStatusEnum` variant -> set on advisory model directly
- Use a match expression or `FromStr` implementation on `AdvisoryStatusEnum` to convert the raw status string from the advisory feed
- Handle unknown status values gracefully with an appropriate error using the `AppError` pattern from `common/src/error.rs`
- Remove any imports of the `advisory_status` entity from the ingestor module

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] Unknown status strings produce a clear error rather than a panic
- [ ] Ingestion pipeline correctly maps all four status values (New, Analyzing, Fixed, Rejected)

## Test Requirements
- [ ] Ingestion of an advisory with each valid status value succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with an unknown status value produces a descriptive error
- [ ] End-to-end ingestion test: ingest an advisory and verify the status is queryable via the advisory list endpoint

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update entity definitions

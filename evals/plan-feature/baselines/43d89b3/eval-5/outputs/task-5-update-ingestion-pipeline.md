## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently parses an advisory from the feed, inserts or looks up the status in the `advisory_status` table, and then uses the resulting ID as `status_id` on the advisory row. After this change, the pipeline maps the status string from the feed directly to an `AdvisoryStatusEnum` value and sets it on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove logic that inserts into or queries the `advisory_status` table; map the status string from the feed to `AdvisoryStatusEnum` and set it directly on the advisory `ActiveModel`

## Implementation Notes
Follow the existing ingestion pattern in `modules/ingestor/src/graph/advisory/mod.rs`. The key change is replacing the status lookup/insert logic:

**Before (current pattern):**
```rust
// Look up or insert status in advisory_status table
let status = advisory_status::ActiveModel {
    value: Set(status_string),
    ..Default::default()
};
let status_id = status.insert(db).await?.id;
// Set status_id on advisory
advisory_model.status_id = Set(status_id);
```

**After (new pattern):**
```rust
// Map status string directly to enum
let status = match status_string.as_str() {
    "New" => AdvisoryStatusEnum::New,
    "Analyzing" => AdvisoryStatusEnum::Analyzing,
    "Fixed" => AdvisoryStatusEnum::Fixed,
    "Rejected" => AdvisoryStatusEnum::Rejected,
    other => return Err(AppError::BadRequest(format!("Unknown advisory status: {}", other))),
};
advisory_model.status = Set(status);
```

Use the `AppError` enum from `common/src/error.rs` for error handling when an unrecognized status string is encountered.

Reference the SBOM ingestion pipeline in `modules/ingestor/src/graph/sbom/mod.rs` for the general ingestion pattern and error handling approach.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion pipeline pattern and error handling
- `modules/ingestor/src/service/mod.rs` — IngestorService structure for understanding the ingestion flow
- `common/src/error.rs` — AppError enum for error handling

## Acceptance Criteria
- [ ] Ingestion pipeline no longer writes to or reads from the `advisory_status` table
- [ ] Ingestion pipeline maps status strings to `AdvisoryStatusEnum` values directly
- [ ] Ingestion pipeline sets `status` enum value on the advisory `ActiveModel`
- [ ] Unrecognized status strings produce a clear error
- [ ] No references to `advisory_status` entity remain in the ingestor module
- [ ] Code compiles with `cargo check -p ingestor`

## Test Requirements
- [ ] `cargo check -p ingestor` passes with no errors
- [ ] Ingestion of an advisory with status "New" correctly sets enum value
- [ ] Ingestion of an advisory with status "Fixed" correctly sets enum value
- [ ] Ingestion of an advisory with an unrecognized status produces an appropriate error

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

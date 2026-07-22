# Task 5 -- Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently parses the status string from the advisory feed, looks up or inserts the status in the lookup table, and writes the resulting ID to `advisory.status_id`. After this change, the pipeline maps the status string directly to an `AdvisoryStatusEnum` variant and writes it to the `advisory.status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace lookup table insert/query logic with direct enum value mapping; update the advisory insert/update to set the `status` enum column instead of `status_id`
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references `advisory_status` entities or lookup logic

## Implementation Notes
- The ingestion pipeline should map the incoming status string to an `AdvisoryStatusEnum` variant using a match expression:
  ```rust
  let status = match status_str.as_str() {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      other => return Err(anyhow!("Unknown advisory status: {}", other)),
  };
  ```
- Remove all code that queries or inserts into the `advisory_status` table.
- When building the `advisory::ActiveModel` for insert, set `status: Set(status_enum_value)` instead of `status_id: Set(status_id_value)`.
- Reference the existing SBOM ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how ingestion modules interact with entity active models.

Per CONVENTIONS.md &sect;Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping for error-producing operations.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's service scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference ingestion pattern for entity insert using ActiveModel
- `common/src/error.rs` -- `AppError` enum for error handling with `.context()` wrapping
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum definition created in Task 3

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status`
- [ ] No ingestion code references the `advisory_status` lookup table
- [ ] Invalid status strings in the feed produce a clear error message
- [ ] Ingested advisories have the correct status enum value stored in the database

## Test Requirements
- [ ] Verify ingestion of an advisory with each of the four valid status values (New, Analyzing, Fixed, Rejected)
- [ ] Verify ingestion of an advisory with an unknown status string produces an appropriate error

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without errors
- `cargo test -p ingestor` -- ingestor tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

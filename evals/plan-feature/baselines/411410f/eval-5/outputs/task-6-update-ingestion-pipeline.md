# Task 6 -- Update advisory ingestion pipeline for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the enum status value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and setting a foreign key. The pipeline currently parses the status from the advisory feed, looks up or inserts the status in the `advisory_status` table, and sets `status_id` on the advisory row. After this change, the pipeline maps the status string directly to an `AdvisoryStatusEnum` variant and writes it to the `status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Replace lookup-table-based status insertion with direct enum value assignment on the advisory `ActiveModel`; remove all references to `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it references `advisory_status` entity for status resolution

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, the current advisory ingestion flow likely:
  1. Parses status string from the feed (e.g., `"Fixed"`)
  2. Queries or inserts into `advisory_status` to get the `id`
  3. Sets `advisory_model.status_id = Set(status_id)` on the advisory `ActiveModel`
  
  Replace this with:
  1. Parse status string from the feed
  2. Map to `AdvisoryStatusEnum` variant (e.g., `AdvisoryStatusEnum::Fixed`)
  3. Set `advisory_model.status = Set(AdvisoryStatusEnum::Fixed)` directly
  
- Use a match expression or `FromStr` implementation to map feed status strings to enum variants. Handle unrecognized status values by returning an error via `AppError` with `.context("unknown advisory status")`.
- Remove any `use entity::advisory_status` imports from both files.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for error handling and model construction conventions.
- The `IngestorService` in `modules/ingestor/src/service/mod.rs` may orchestrate the advisory ingestion -- verify it does not directly reference `advisory_status` entity.

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` value directly to `advisory.status` column
- [ ] No lookup table query or insertion for advisory status during ingestion
- [ ] Unrecognized status strings from the feed produce a clear error
- [ ] No remaining references to `advisory_status` entity in the ingestor module
- [ ] `cargo build -p ingestor` compiles without errors

## Test Requirements
- [ ] Test ingesting an advisory with status "New" -- verify `advisory.status` is `AdvisoryStatusEnum::New`
- [ ] Test ingesting an advisory with status "Fixed" -- verify `advisory.status` is `AdvisoryStatusEnum::Fixed`
- [ ] Test ingesting an advisory with an unrecognized status -- verify error is returned
- [ ] Verify no writes to the (now-dropped) `advisory_status` table during ingestion

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

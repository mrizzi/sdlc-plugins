# Task 5: Update advisory ingestion pipeline to write enum values directly

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory ingestion pipeline to write the status as an enum value directly to the `advisory.status` column, instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion code must map incoming status strings to `AdvisoryStatusEnum` variants and set them on the advisory entity during insert.

## Acceptance Criteria

- The advisory ingestion code no longer writes to or references the `advisory_status` table
- Incoming status strings are mapped to `AdvisoryStatusEnum` variants
- Advisory records are inserted with the `status` enum column populated directly
- Invalid status strings produce a clear error (not a database constraint violation)
- Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) works correctly

## Test Requirements

- Integration test that ingests an advisory with each valid status value and verifies the `status` column is set correctly
- Test that ingesting an advisory with an invalid status string returns an appropriate error
- Verify no writes to the former `advisory_status` table occur during ingestion

## Files to Modify

- `modules/ingestor/src/graph/advisory/mod.rs` -- remove `advisory_status` table writes; map status strings to `AdvisoryStatusEnum` and set on advisory entity directly
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references `advisory_status` entity or status lookup logic

## Implementation Notes

- The current ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` likely inserts a row into `advisory_status` (or looks up an existing one) and then sets `status_id` on the advisory -- replace this with direct enum assignment
- Use `AdvisoryStatusEnum::from_str()` or a match statement to convert the incoming status string to the enum variant
- Import `AdvisoryStatusEnum` from the entity crate
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for the insert/update flow
- Ensure the `IngestorService` in `modules/ingestor/src/service/mod.rs` does not maintain any cached references to the removed lookup table

## Dependencies

- Task 1: Create feature branch TC-9005 from main
- Task 3: Update SeaORM entity definitions for advisory status enum

[Description digest: sha256-md:e7c5b1a2f6d38c0a45ja2e8b1f7c6d534a0b2c8e9f1a4b5c6d7e8f9a0b1c2d34 would be posted as a comment]

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `AdvisoryStatusEnum` value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently parses the advisory status string from the feed, looks up or creates a row in `advisory_status`, and stores the `status_id` on the advisory record. After this change, the pipeline maps the status string directly to an `AdvisoryStatusEnum` variant and writes it to the `status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK reference with direct `AdvisoryStatusEnum` value assignment; remove any `advisory_status` entity imports and related insertion logic
- `modules/ingestor/src/service/mod.rs` — verify `IngestorService` does not reference `advisory_status` entity (update if it does)

## Implementation Notes
The advisory ingestion flow currently performs these steps for status:
1. Parse status string from the advisory feed
2. Look up or insert a row in `advisory_status` table
3. Store the resulting `status_id` on the advisory record

Replace with:
1. Parse status string from the advisory feed
2. Map to `AdvisoryStatusEnum` variant (e.g., `"Fixed"` -> `AdvisoryStatusEnum::Fixed`)
3. Set the `status` field directly on the advisory `ActiveModel`

Add a validation step that rejects advisory records with unrecognized status values rather than silently failing. Use a `match` expression with an explicit error for unknown status strings:
```rust
let status = match status_str.as_str() {
    "New" => AdvisoryStatusEnum::New,
    "Analyzing" => AdvisoryStatusEnum::Analyzing,
    "Fixed" => AdvisoryStatusEnum::Fixed,
    "Rejected" => AdvisoryStatusEnum::Rejected,
    other => return Err(AppError::from(anyhow!("Unknown advisory status: {}", other))),
};
```

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all error-producing operations in the ingestion pipeline.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern for reference on how to structure entity insertion without lookup table indirection
- `common/src/error.rs` — `AppError` enum for error handling in ingestion failure cases

## Acceptance Criteria
- [ ] The advisory ingestion pipeline writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] The pipeline no longer inserts into or references the `advisory_status` lookup table
- [ ] Unrecognized status strings produce a clear error rather than silently failing
- [ ] All four valid status values (`New`, `Analyzing`, `Fixed`, `Rejected`) are correctly mapped during ingestion

## Test Requirements
- [ ] Ingestion of an advisory with status `"Fixed"` writes `AdvisoryStatusEnum::Fixed` to the `status` column
- [ ] Ingestion of an advisory with an unrecognized status string returns an error
- [ ] Ingestion of advisories with all four valid status values succeeds

## Verification Commands
- `cargo build -p ingestor` — ingestor module compiles without errors
- `cargo test -p ingestor` — ingestor module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

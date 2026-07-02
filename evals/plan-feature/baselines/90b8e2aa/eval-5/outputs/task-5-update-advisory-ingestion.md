# Task 5 — Update advisory ingestion pipeline for enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting a row into the `advisory_status` lookup table and then referencing it by FK. The pipeline must map incoming status strings from the advisory feed to `AdvisoryStatusEnum` variants.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert and FK assignment with direct enum value write; add mapping from feed status strings to `AdvisoryStatusEnum` variants

## Implementation Notes
- The current ingestion flow likely: (1) inserts or looks up the status string in `advisory_status`, (2) gets the `status_id`, (3) sets `advisory.status_id`. Replace this with a direct mapping from the feed's status string to `AdvisoryStatusEnum` and set `advisory.status` on the advisory `ActiveModel`.
- Use a match expression to map feed status strings to `AdvisoryStatusEnum` variants:
  ```rust
  let status = match status_str.as_str() {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      other => return Err(anyhow!("Unknown advisory status: {}", other)),
  };
  ```
- Remove any code that queries or inserts into the `advisory_status` table.
- Follow the pattern established in SBOM ingestion (`modules/ingestor/src/graph/sbom/mod.rs`) for how ingestion writes entity fields directly.
- Per CONVENTIONS.md §Framework: use SeaORM `ActiveModel` and `ActiveValue::Set()` for setting the enum field.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's database framework scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module demonstrating the pattern for parsing feed data and writing entity fields via SeaORM ActiveModel
- `modules/ingestor/src/service/mod.rs::IngestorService` — ingestion service entry point showing the ingestion orchestration pattern

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] No code references the `advisory_status` lookup table in the ingestion pipeline
- [ ] Status string mapping handles all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Invalid status strings produce a clear error rather than a silent failure
- [ ] The ingestion module compiles without errors (`cargo check -p ingestor`)

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" writes the correct enum value
- [ ] Verify ingestion with an unknown status string produces an appropriate error
- [ ] Verify ingestion does not attempt to insert into or query the `advisory_status` table

## Verification Commands
- `cargo check -p ingestor` — compiles without errors
- `cargo test -p ingestor` — existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

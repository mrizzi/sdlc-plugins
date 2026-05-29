# Task 5 -- Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion pipeline currently writes status to the lookup table first, then stores the `status_id` on the advisory record. After this change, the pipeline maps the incoming status string to the `AdvisoryStatusEnum` variant and writes it directly.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- update advisory ingestion logic to map status strings to `AdvisoryStatusEnum` variants and write the enum value directly to the `advisory.status` column; remove any logic that inserts into or queries the `advisory_status` lookup table
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it contains advisory status handling logic that references the lookup table
- `modules/ingestor/Cargo.toml` -- add dependency on the `entity` crate if not already present, to access `AdvisoryStatusEnum`

## Implementation Notes
- The ingestion pipeline at `modules/ingestor/src/graph/advisory/mod.rs` currently does something like:
  1. Parse status string from advisory feed
  2. Look up or insert status in `advisory_status` table to get `status_id`
  3. Insert advisory with `status_id` FK
- Replace this with:
  1. Parse status string from advisory feed
  2. Map status string to `AdvisoryStatusEnum` variant (handle case-insensitive matching and unknown values gracefully)
  3. Insert advisory with `status` enum value directly
- For mapping, implement a `FromStr` or `TryFrom<&str>` for `AdvisoryStatusEnum` that handles the expected input values from the advisory feed. If the enum already derives `DeriveActiveEnum` with `string_value` attributes, SeaORM may provide this automatically.
- Handle edge cases: if the feed contains an unrecognized status value, return an appropriate error rather than silently dropping it. Follow the existing error handling pattern using `AppError` from `common/src/error.rs` with `.context()` wrapping.
- Reference the SBOM ingestion pattern at `modules/ingestor/src/graph/sbom/mod.rs` for the general ingestion flow.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference for ingestion flow patterns (parse, store, link)
- `common/src/error.rs` -- `AppError` enum for error handling patterns
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No remaining references to `advisory_status` lookup table in the ingestion pipeline
- [ ] Unknown status values in the feed produce a clear error (not a silent failure)
- [ ] The ingestor module compiles without errors

## Test Requirements
- [ ] Advisory ingestion correctly maps known status strings (New, Analyzing, Fixed, Rejected) to enum values
- [ ] Advisory ingestion returns an error for unrecognized status strings
- [ ] End-to-end ingestion test: ingest a sample advisory with a known status, then query the advisory and verify the `status` field is correct

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without errors
- `cargo test -p tests --test advisory` -- advisory integration tests pass including ingestion scenarios

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

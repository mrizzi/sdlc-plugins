## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and storing a foreign key. The ingestion module currently parses advisory feeds, maps status strings to lookup table rows, and stores the `status_id` on the advisory record. After this change, the pipeline will map status strings directly to `AdvisoryStatusEnum` variants and insert them into the `status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — update advisory ingestion logic: replace lookup table insert + FK assignment with direct `AdvisoryStatusEnum` value assignment; update the status mapping function to convert feed status strings to enum variants
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity or lookup table operations

## Implementation Notes
- In `graph/advisory/mod.rs`, locate the code that currently: (1) looks up or inserts a status row in `advisory_status`, (2) stores the returned `id` as `status_id` on the advisory record. Replace this with: (1) map the feed status string to an `AdvisoryStatusEnum` variant, (2) set `advisory::ActiveModel { status: Set(enum_variant), ... }`.
- Handle invalid status strings gracefully — if the feed contains an unrecognized status value, return an appropriate error rather than silently defaulting. Use `AppError` from `common/src/error.rs` for consistent error handling.
- Follow the ingestion patterns in `modules/ingestor/src/graph/sbom/mod.rs` for structure and error handling consistency.
- Import `AdvisoryStatusEnum` from the entity crate: `use entity::advisory::AdvisoryStatusEnum;`
- Per `docs/constraints.md` §5.4: do not duplicate existing error handling patterns — reuse `AppError` from `common/src/error.rs`.
- Per `docs/constraints.md` §5.2: inspect existing ingestion code before modifying.
- Per `docs/constraints.md` §2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion module demonstrating the project's ingestion pattern
- `common/src/error.rs` — `AppError` for consistent error handling
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type to use for status values

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status`
- [ ] No references to `advisory_status` entity or lookup table remain in the ingestor module
- [ ] Invalid status strings from feeds produce clear error messages
- [ ] The ingestor module compiles without errors

## Test Requirements
- [ ] Verify the ingestor module compiles: `cargo check -p ingestor`
- [ ] Verify that ingesting an advisory with each valid status value (New, Analyzing, Fixed, Rejected) succeeds
- [ ] Verify that ingesting an advisory with an invalid status value produces an appropriate error

## Verification Commands
- `cargo check -p ingestor` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
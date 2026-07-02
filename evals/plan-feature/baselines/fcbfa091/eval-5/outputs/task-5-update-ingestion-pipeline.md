# Task 5: Update advisory ingestion pipeline

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion module currently parses advisory feeds, resolves the status string to an `advisory_status` row ID, and sets `status_id` on the advisory insert. After this change, the pipeline maps the status string directly to an `AdvisoryStatusEnum` variant and sets the `status` column on insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace lookup table insert/reference logic with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it contains any status resolution logic that references the lookup table

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the current ingestion flow likely:
1. Parses status string from the advisory feed
2. Looks up or inserts a row in `advisory_status` to get the `status_id`
3. Sets `status_id` on the `advisory` ActiveModel

Replace this with:
1. Parse status string from the advisory feed
2. Map to `AdvisoryStatusEnum` variant using `match` or `FromStr`
3. Set `status` on the `advisory` ActiveModel directly

Add validation to reject unknown status strings with a descriptive error using `.context()` wrapping, following the error handling pattern in the existing ingestion code.

The enum type `AdvisoryStatusEnum` is defined in `entity/src/advisory_status_enum.rs` (created in Task 3) and should be imported from the entity crate.

Per CONVENTIONS.md Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `entity/src/advisory_status_enum.rs::AdvisoryStatusEnum` -- the enum type to map incoming status strings to; import from entity crate

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to `advisory.status`
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] Unknown status strings produce a descriptive error with `.context()` wrapping
- [ ] Advisory ingestion creates advisory rows with correct enum status values

## Test Requirements
- [ ] Ingestion of an advisory with status "New" writes `AdvisoryStatusEnum::New` to the database
- [ ] Ingestion of an advisory with status "Fixed" writes `AdvisoryStatusEnum::Fixed`
- [ ] Ingestion of an advisory with an unknown status produces an error
- [ ] `cargo build -p ingestor` compiles successfully

## Verification Commands
- `cargo build -p ingestor` -- ingestor crate compiles without errors
- `cargo test -p ingestor` -- ingestor tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0

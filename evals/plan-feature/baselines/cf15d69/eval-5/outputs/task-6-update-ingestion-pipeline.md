## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline must map incoming status strings to the `AdvisoryStatusEnum` Rust enum and set the field on the advisory entity directly.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace lookup table insert-or-fetch logic for status with direct enum value assignment; map the incoming status string to `AdvisoryStatusEnum` variant and set it on the advisory `ActiveModel`
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references advisory status lookup table operations or passes `status_id` to downstream functions

## Implementation Notes
- The current ingestion flow likely: (1) parses a status string from the advisory feed, (2) looks up or inserts the status in `advisory_status` table, (3) sets `status_id` on the advisory row. Replace steps 2-3 with: parse the status string, convert to `AdvisoryStatusEnum` using `FromStr` or a match expression, and set `status` on the advisory `ActiveModel`
- Handle unknown status values gracefully — if the feed contains a status not in the enum, either reject the advisory with a descriptive error or default to `New` (document the decision)
- Import `AdvisoryStatusEnum` from the entity crate
- Remove any `use` imports of the old `advisory_status` entity

Per Key Conventions (Error handling): All service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` and `modules/ingestor/src/service/mod.rs` matching the service/graph scope.

## Acceptance Criteria
- [ ] Advisory ingestion writes enum value directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] Unknown status values are handled with a clear error or documented default
- [ ] Ingestion of advisories with all four valid statuses succeeds
- [ ] The ingestor module compiles without errors

## Test Requirements
- [ ] Verify the ingestor module compiles: `cargo check -p trustify-module-ingestor`
- [ ] Verify ingestion of an advisory with status "Fixed" produces the correct enum value in the database
- [ ] Verify ingestion of an advisory with an unknown status produces a clear error

## Verification Commands
```bash
cargo check -p trustify-module-ingestor
```

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions

[sdlc-workflow] Description digest: sha256-md:12ec904ffe31e92430384f032f3dfdf6971c5e947c71665b04bc6a5f428f777e

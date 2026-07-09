## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion pipeline must map incoming status strings from the advisory feed to the appropriate enum variant.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace lookup table insert and FK reference with direct enum value assignment when creating or updating advisory records

## Implementation Notes
- Remove any code that inserts rows into the `advisory_status` table during advisory ingestion.
- Remove any code that queries the `advisory_status` table to resolve a status string to a `status_id` integer.
- Map incoming status strings from the advisory feed directly to `AdvisoryStatusEnum` variants. Implement a `match` expression or `FromStr`/`TryFrom<&str>` conversion to map the feed's status string (e.g., "Fixed", "New") to the corresponding enum variant.
- When creating or updating advisory `ActiveModel` instances, set the `status` field to `Set(AdvisoryStatusEnum::Fixed)` (or the appropriate variant) instead of `Set(status_id)`.
- Handle unknown status strings gracefully -- log a warning and either skip the advisory or default to `AdvisoryStatusEnum::New`, following the existing error handling pattern in the ingestion module.
- Remove any `use` imports referencing the `advisory_status` entity.
- Per CONVENTIONS.md §Module pattern: follow the established `model/ + service/ + endpoints/` structure within the ingestor module.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's ingestor module file scope.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the established ingestion pattern for inserting records with direct column values.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- sibling ingestion module demonstrating the standard ingestion pattern for parsing input, creating entity records, and error handling
- `entity/src/advisory.rs` -- the updated advisory entity with the `AdvisoryStatusEnum` type definition used for setting the status field

## Acceptance Criteria
- [ ] Advisory ingestion writes enum status value directly to `advisory.status` column
- [ ] No code references the `advisory_status` lookup table during ingestion
- [ ] All four status values (New, Analyzing, Fixed, Rejected) are correctly mapped from feed input
- [ ] Unknown status strings are handled gracefully without crashing the ingestion pipeline

## Test Requirements
- [ ] Verify ingestion of an advisory with status "Fixed" stores `AdvisoryStatusEnum::Fixed` in the database
- [ ] Verify ingestion of an advisory with status "New" stores `AdvisoryStatusEnum::New`
- [ ] Verify ingestion of an advisory with each of the four status values produces correct enum storage
- [ ] Verify ingestion handles an advisory with an unknown status string gracefully (warning logged, no crash)

## Verification Commands
- `cargo test -p ingestor` -- ingestor module tests pass
- `cargo build -p ingestor` -- module compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum

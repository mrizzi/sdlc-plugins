## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `status` column on the `advisory` table, instead of first inserting into the `advisory_status` lookup table and then referencing the lookup row via foreign key. This simplifies the ingestion flow and removes the dependency on the now-dropped lookup table.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — update advisory ingestion logic to map status strings from the feed to `AdvisoryStatusEnum` values and insert them directly into the `status` column; remove any code that inserts into or queries the `advisory_status` table

## Implementation Notes
- In the advisory ingestion module (`graph/advisory/mod.rs`), locate the code path that currently: (a) looks up or inserts a status row in `advisory_status`, (b) retrieves the `id`, and (c) sets `status_id` on the advisory insert. Replace this with a direct mapping from the feed's status string to the `AdvisoryStatusEnum` variant.
- Use a match expression or `FromStr` implementation on `AdvisoryStatusEnum` to convert feed status strings to enum variants. Handle unknown status values explicitly — either reject the advisory with an error or default to a sensible variant with a warning log.
- Remove any `use` imports of `advisory_status::Entity` or `advisory_status::ActiveModel` from the ingestion module.
- Reference the SBOM ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for the expected ingestion code structure.
- Ensure error handling follows the project pattern: return `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`).
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing ingestion code before modifying; follow established patterns.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion code structure and patterns
- `common/src/error.rs` — `AppError` enum for consistent error handling with `.context()` wrapping

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `status` column
- [ ] No ingestion code references the `advisory_status` table or its entity
- [ ] Unknown status values from feeds are handled gracefully (error or default with warning)
- [ ] Ingestion module compiles without errors

## Test Requirements
- [ ] Run `cargo build -p ingestor` to verify compilation
- [ ] Run `cargo test -p ingestor` to verify no test regressions
- [ ] Verify ingestion correctly maps status strings to enum variants

## Verification Commands
- `cargo build -p ingestor` — expected: compiles without errors
- `cargo test -p ingestor` — expected: all existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

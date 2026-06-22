# Task 5 — Update advisory ingestion pipeline to write enum status directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline should map incoming status strings to `AdvisoryStatusEnum` variants and set the enum value during advisory row insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove logic that inserts/upserts into the `advisory_status` table; replace `status_id` assignment with direct `status: AdvisoryStatusEnum` assignment; update the advisory insert/upsert ActiveModel to use the enum field
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains any status-related logic that references the lookup table

## Implementation Notes
- The current ingestion flow likely follows this pattern: (1) look up or insert status string in `advisory_status` table, (2) get the returned `id`, (3) set `status_id` on the advisory `ActiveModel`. After this change, the flow simplifies to: (1) parse status string to `AdvisoryStatusEnum` variant, (2) set `status` on the advisory `ActiveModel`.
- Create a helper function or `impl From<String>` / `impl FromStr` on `AdvisoryStatusEnum` to map incoming status strings from advisory feeds to enum variants. Handle invalid status strings with an appropriate error rather than silently defaulting.
- Reference the SBOM ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for the established ingestion flow structure in this project.
- Remove any `use entity::advisory_status` imports from the ingestion module.
- Per docs/constraints.md §5.2: inspect `modules/ingestor/src/graph/advisory/mod.rs` before modifying to understand the current status insertion logic.
- Per docs/constraints.md §5.4: reuse the `AdvisoryStatusEnum` type defined in the entity crate (Task 3) rather than defining a duplicate enum.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3; import and use directly rather than defining a separate mapping
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion graph module patterns (parse, store, link)

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to `advisory.status` without any interaction with the `advisory_status` table
- [ ] Invalid status strings in advisory feeds produce a clear error (not a silent default or panic)
- [ ] No references to `advisory_status` entity or table remain in the ingestor module
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify the ingestor module compiles: `cargo check -p ingestor`
- [ ] Test that ingesting an advisory with a valid status (e.g., "New") correctly sets the enum value
- [ ] Test that ingesting an advisory with an invalid status string produces an appropriate error

## Verification Commands
- `cargo check -p ingestor` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

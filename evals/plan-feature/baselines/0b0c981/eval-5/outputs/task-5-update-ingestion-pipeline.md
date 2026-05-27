## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline should map incoming status strings from advisory feeds to `AdvisoryStatusEnum` variants and set the enum value directly on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK reference with direct enum value assignment on the advisory entity

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, locate the code that currently: (1) looks up or inserts a row in `advisory_status` table, (2) retrieves the `id`, and (3) sets `status_id` on the advisory entity. Replace this with direct assignment of `AdvisoryStatusEnum` variant to the advisory's `status` field.
- Map incoming status strings to enum variants: `"New"` -> `AdvisoryStatusEnum::New`, `"Analyzing"` -> `AdvisoryStatusEnum::Analyzing`, `"Fixed"` -> `AdvisoryStatusEnum::Fixed`, `"Rejected"` -> `AdvisoryStatusEnum::Rejected`.
- Handle unknown status strings gracefully — either default to `AdvisoryStatusEnum::New` or return an error, depending on the existing error handling pattern in the ingestion pipeline. Inspect the current error handling in `modules/ingestor/src/graph/advisory/mod.rs` before deciding.
- Follow the existing ingestion patterns in `modules/ingestor/src/graph/sbom/mod.rs` for how entities are constructed and inserted.
- Per constraints §5.2: inspect existing ingestion code before modifying. Per §5.4: reuse existing error handling patterns.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference pattern for entity construction and insertion during ingestion
- `modules/ingestor/src/service/mod.rs` — `IngestorService` orchestration pattern for how ingestion operations are coordinated

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No code references the `advisory_status` lookup table for ingestion
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unknown status strings are handled gracefully (error or default, consistent with existing patterns)
- [ ] Ingestor crate compiles without errors (`cargo check -p ingestor`)

## Test Requirements
- [ ] Ingestion of an advisory with each valid status value produces the correct enum value in the database
- [ ] Ingestion of an advisory with an unknown status string is handled gracefully (does not panic)

## Verification Commands
- `cargo check -p ingestor` — ingestor crate compiles cleanly
- `cargo test -p ingestor` — ingestor tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:a77ff9bc38e5ca7851c781b351554635dd67b50c8a6535df57b24d7b1409e813

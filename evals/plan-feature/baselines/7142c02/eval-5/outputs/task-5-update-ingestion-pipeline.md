## Repository
trustify-backend

## Target Branch
TC-9005

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline must map incoming status strings from advisory feeds to `advisory_status_enum` values.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace lookup table insert + FK reference with direct enum value write for advisory status

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, locate the advisory ingestion logic that currently:
  1. Checks if a status row exists in `advisory_status` (or inserts one)
  2. Gets the `advisory_status.id`
  3. Sets `advisory.status_id = <id>`
- Replace this with direct enum mapping:
  1. Parse the status string from the advisory feed
  2. Map it to an `AdvisoryStatusEnum` variant (New, Analyzing, Fixed, Rejected)
  3. Set `advisory.status = <enum_value>` directly
- Add validation for unrecognized status strings — log a warning and either reject the advisory or default to a sensible status (e.g., `New`), following the error handling pattern in `common/src/error.rs`
- Reference the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for SBOM ingestion to follow consistent ingestion patterns
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pipeline; reference for ingestion flow patterns and error handling
- `modules/ingestor/src/service/mod.rs` — `IngestorService`; reference for how ingestion services are structured

## Acceptance Criteria
- [ ] Advisory ingestion writes enum status value directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Unrecognized status strings are handled gracefully (logged and defaulted)
- [ ] Ingested advisories have correct status values when queried

## Test Requirements
- [ ] Ingestion of advisory with each valid status value (New, Analyzing, Fixed, Rejected) sets correct enum value
- [ ] Ingestion of advisory with unrecognized status string is handled gracefully
- [ ] End-to-end ingestion test: ingest advisory, query it, verify status is correct enum value

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:cffca02dbd31eeb15a75a5cf789291723bfcbdcd064e93d7ca34c1894c6073be

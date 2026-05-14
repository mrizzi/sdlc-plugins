## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation method to `SbomService` that queries the database for advisory
severity counts associated with a given SBOM. The method joins the `sbom_advisory` and
`advisory` tables, deduplicates by advisory ID, groups by severity level, and returns an
`AdvisorySeveritySummary`. This is the core data-access logic for the advisory-summary
endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing query patterns in `SbomService` at `modules/fundamental/src/sbom/service/sbom.rs` — the `fetch`, `list`, and `ingest` methods demonstrate how to construct SeaORM queries and handle errors.
- Use the `sbom_advisory` join entity at `entity/src/sbom_advisory.rs` to join SBOMs to advisories. The `advisory` entity at `entity/src/advisory.rs` contains the severity field.
- The query should:
  1. Filter `sbom_advisory` rows by the given `sbom_id`
  2. Join to the `advisory` table to access the `severity` field
  3. Select distinct advisory IDs to avoid double-counting (same advisory linked multiple times)
  4. Group by severity and count occurrences
  5. Map the grouped counts into `AdvisorySeveritySummary` fields
- Return a 404 `AppError` if the SBOM ID does not exist. Check SBOM existence first using the existing `fetch` method on `SbomService`, consistent with how `GET /api/v2/sbom/{id}` validates the ID (see `modules/fundamental/src/sbom/endpoints/get.rs`).
- Use the shared query helpers in `common/src/db/query.rs` if any filtering or pagination utilities are applicable.
- Error handling: wrap database errors with `.context()` per the pattern in `common/src/error.rs` and `AppError` conventions.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect existing code before modifying, follow patterns in Implementation Notes, and do not duplicate existing functionality.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — pattern for SBOM existence validation and error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — pattern for querying advisory data and joining related tables
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation, context wrapping pattern

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model

## Acceptance Criteria
- [ ] `SbomService` has a new public method `advisory_severity_summary` that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The query deduplicates advisories by advisory ID before counting
- [ ] The query correctly groups counts into critical, high, medium, low categories
- [ ] The `total` field equals the sum of all severity counts
- [ ] Returns 404 `AppError` when the SBOM ID does not exist in the database
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit test: verify the method returns correct severity counts for an SBOM with known advisory associations (requires test database fixtures)
- [ ] Unit test: verify the method returns 404 error for a non-existent SBOM ID
- [ ] Unit test: verify deduplication — an advisory linked to the same SBOM twice is counted only once

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

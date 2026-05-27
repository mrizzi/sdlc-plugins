## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation query method to `SbomService` that counts unique advisories by severity level for a given SBOM. This method queries the `sbom_advisory` join table, groups by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists and returns an appropriate error if not found.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). Existing methods like `fetch` and `list` demonstrate the standard pattern: accept a database connection/transaction parameter, use SeaORM query builders, and return `Result<T, AppError>` with `.context()` wrapping for error handling (see `common/src/error.rs` for `AppError`).

The aggregation query should:
1. First verify the SBOM exists by querying the `sbom` entity (`entity/src/sbom.rs`). If not found, return a 404-equivalent `AppError`.
2. Query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) filtering by `sbom_id`.
3. Join with the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
4. Use `SELECT COUNT(DISTINCT advisory_id)` grouped by severity to deduplicate advisories.
5. Map the grouped results into `AdvisorySeveritySummary` fields.
6. Compute `total` as the sum of all severity counts.

Use the shared query builder helpers from `common/src/db/query.rs` if applicable for filtering. Reference the existing `AdvisoryService` methods in `modules/fundamental/src/advisory/service/advisory.rs` for patterns on querying advisory-related entities.

Per constraints §5.2: inspect `sbom.rs` service, entity files, and `AppError` before implementing.
Per constraints §5.4: reuse existing query helpers from `common/src/db/query.rs` rather than duplicating filtering logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct; add the new method here following established patterns for error handling and DB access
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse for any query construction
- `common/src/error.rs::AppError` — Error enum with `IntoResponse` impl; use for 404 and internal error cases
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; the primary table for the aggregation query
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference for advisory entity query patterns

## Acceptance Criteria
- [ ] `SbomService` has a new method `get_advisory_severity_summary` that returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method returns correct severity counts for a given SBOM by querying `sbom_advisory` and `advisory` entities
- [ ] Advisory IDs are deduplicated (each advisory counted once even if linked multiple times)
- [ ] Method returns a 404-equivalent `AppError` when the SBOM does not exist
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Unit/integration test: verify correct severity counts for an SBOM with known advisory data
- [ ] Unit/integration test: verify deduplication — an advisory linked multiple times is counted once
- [ ] Unit/integration test: verify 404 error when querying a non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model


[sdlc-workflow] Description digest: sha256:09b1e888adc5540162e0d0bbe96fd2754731e148eb1f2d522c02a6978dacaec7

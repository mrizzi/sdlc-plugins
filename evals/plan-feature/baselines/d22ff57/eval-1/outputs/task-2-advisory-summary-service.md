# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Description
Add a service method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table to retrieve severity, deduplicates by advisory ID, and returns aggregated counts grouped by severity level. This method powers the new advisory-summary endpoint and must meet the p95 < 200ms performance target for SBOMs with up to 500 advisories.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<Severity>, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## API Changes
- Internal service API — NEW: `SbomService::advisory_severity_summary(sbom_id, threshold, db)` returns `Result<AdvisorySeveritySummary, AppError>`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods like `fetch` and `list`). Each method takes a database connection, uses SeaORM query builders, and returns `Result<T, AppError>` with `.context()` error wrapping.
- Use the `entity/src/sbom_advisory.rs` join table entity to query advisory-SBOM relationships. Join to `entity/src/advisory.rs` to access the severity field.
- Deduplication: Use `SELECT DISTINCT advisory_id` or `GROUP BY advisory_id` in the query to ensure each advisory is counted only once even if linked to the SBOM through multiple paths.
- Aggregation: Use a SQL `COUNT(*) ... GROUP BY severity` query via SeaORM, or fetch distinct advisories and count in application code. Prefer database-side aggregation for performance.
- The `threshold` parameter (optional) filters to only include advisories at or above the specified severity level. Severity ordering: Critical > High > Medium > Low. When threshold is provided, counts below the threshold should be zero and total should reflect only the filtered counts.
- Return `AppError` with 404 status if the SBOM ID does not exist. Check SBOM existence before running the aggregation query, consistent with existing SBOM endpoints (`get.rs` handler pattern).
- No new database tables are required — use existing `sbom_advisory` and `advisory` entities per the non-functional requirements.
- Per `docs/constraints.md` §5.2: Inspect `sbom.rs` service file before modifying to understand the exact method signatures, imports, and error handling patterns used.
- Per `docs/constraints.md` §5.4: Reuse existing query helpers from `common/src/db/query.rs` if applicable to filtering logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with fetch/list methods demonstrating the query pattern, error handling, and database connection usage
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; may provide utilities for building the aggregation query
- `common/src/error.rs::AppError` — Error enum with `IntoResponse` implementation; use for 404 and internal error cases
- `entity/src/sbom_advisory.rs` — Join table entity linking SBOMs to advisories
- `entity/src/advisory.rs` — Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary` method exists and compiles
- [ ] Method returns correct severity counts for a given SBOM ID with deduplicated advisories
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method supports optional threshold filtering
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit/integration test verifying correct severity counts for an SBOM with known advisories at each severity level
- [ ] Test verifying deduplication — same advisory linked multiple times is counted once
- [ ] Test verifying 404 is returned for a non-existent SBOM ID
- [ ] Test verifying threshold filtering returns only counts at or above the specified severity

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation method to `SbomService` that queries the database for advisory severity counts associated with a given SBOM. The method joins the `sbom_advisory` join table with the `advisory` table, deduplicates by advisory ID, groups by severity, and returns an `AdvisorySeveritySummary`. This is the core business logic for the advisory-summary endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for method signatures, error handling, and database access patterns.
- Use SeaORM query builder to join `entity::sbom_advisory` with `entity::advisory` on the advisory ID, filter by the given SBOM ID, and use `SELECT COUNT(DISTINCT advisory.id), advisory.severity` with `GROUP BY severity`.
- Reference `entity/src/sbom_advisory.rs` for the join table schema and `entity/src/advisory.rs` for the advisory entity including the severity field.
- Return 404 (`AppError::NotFound`) if the SBOM ID does not exist. Check SBOM existence first using the existing fetch pattern in `SbomService` (look at the `fetch` or `get` method for the established pattern).
- Use `common/src/db/query.rs` query builder helpers where applicable for constructing the aggregation query.
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping on database errors. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- Map severity strings from the database to the struct fields: count advisories where severity = "critical", "high", "medium", "low". Compute `total` as the sum of all four counts.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct; add the new method here following established patterns for database queries and error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how advisory queries are structured, particularly joins and filtering
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; may provide reusable building blocks for the aggregation query
- `common/src/error.rs::AppError` — error type for 404 and internal error responses

## Acceptance Criteria
- [ ] `SbomService` has a new `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns correct counts grouped by severity level (critical, high, medium, low)
- [ ] Method returns `total` as the sum of all severity counts
- [ ] Method returns 404 error if the SBOM ID does not exist
- [ ] Database errors are wrapped with `.context()` per error handling conventions

## Test Requirements
- [ ] Unit/integration test: given an SBOM with known advisories at various severity levels, verify correct counts are returned
- [ ] Test: given an SBOM with duplicate advisories (same advisory linked multiple times), verify deduplication produces correct counts
- [ ] Test: given a non-existent SBOM ID, verify 404 error is returned
- [ ] Test: given an SBOM with zero advisories, verify all counts are 0

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

[sdlc-workflow] Description digest: sha256-md:07eb40ba4264c76eec1c6d3d87772899463f61fba509cad077a4392cc3bac52b

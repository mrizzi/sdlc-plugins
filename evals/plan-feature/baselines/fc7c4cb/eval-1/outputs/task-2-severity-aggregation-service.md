## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the advisory-SBOM relationship table, deduplicates advisories by ID, groups them by severity level, and returns an `AdvisorySeveritySummary` with the counts. This method forms the core business logic for the advisory severity aggregation feature.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to SbomService

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest) for method signatures, error handling with `.context()`, and database query patterns.
- Use the `entity::sbom_advisory` join table entity from `entity/src/sbom_advisory.rs` to query advisories linked to the given SBOM ID. Join with `entity::advisory` from `entity/src/advisory.rs` to access the severity field.
- Deduplicate advisories by advisory ID before counting — use `SELECT DISTINCT advisory_id` or equivalent SeaORM query to avoid counting the same advisory multiple times.
- Group results by severity and count each group. The severity field definition is in `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) — inspect this to determine the exact severity enum/type and its variants.
- Use query builder helpers from `common/src/db/query.rs` where applicable for filtering.
- Return `AppError` with appropriate context on database errors, following the pattern in `common/src/error.rs`.
- Before computing counts, verify the SBOM exists by calling the existing fetch method on SbomService. Return a 404-equivalent error (using the existing AppError variant for not-found) if the SBOM ID does not exist.
- Compute `total` as the sum of all severity counts rather than a separate query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with established patterns for database queries, error handling, and method signatures
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with IntoResponse implementation; reuse existing not-found variant
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService` has a new `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns correct counts for critical, high, medium, and low severity levels
- [ ] Method returns 404-equivalent error when SBOM ID does not exist
- [ ] Total field equals the sum of critical + high + medium + low counts
- [ ] Error handling uses `.context()` wrapping consistent with sibling methods

## Test Requirements
- [ ] Unit or integration test: SBOM with advisories at multiple severity levels returns correct per-level counts
- [ ] Unit or integration test: SBOM with duplicate advisories (same advisory linked multiple times) returns deduplicated counts
- [ ] Unit or integration test: SBOM with zero advisories returns all-zero counts
- [ ] Unit or integration test: non-existent SBOM ID returns not-found error

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

[sdlc-workflow] Description digest: sha256:15646ca6e8665ce27bdee19f851b2482ec371a50810a46a7a652a57962c8c1b0

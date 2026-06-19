## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that aggregates advisory severity counts for a given SBOM ID. The method must query the `sbom_advisory` join table to find all advisories linked to the SBOM, deduplicate by advisory ID, look up each advisory's severity from the advisory entity, count by severity level (Critical, High, Medium, Low), and return an `AdvisorySeveritySummary`. It must return a 404-compatible error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_summary(&self, sbom_id: Uuid, threshold: Option<String>) -> Result<AdvisorySeveritySummary, AppError>` method to SbomService

## Implementation Notes
- Follow the existing service patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest) for method signatures, error handling, and database interaction style.
- Use SeaORM query builder to join `sbom_advisory` (entity at `entity/src/sbom_advisory.rs`) with `advisory` (entity at `entity/src/advisory.rs`) to aggregate severity counts. Use `GROUP BY severity` with `COUNT(DISTINCT advisory_id)` to deduplicate.
- First verify the SBOM exists by querying the `sbom` entity (`entity/src/sbom.rs`). If not found, return an error that maps to HTTP 404, consistent with existing SBOM endpoints like the get handler in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Use the shared query helpers from `common/src/db/query.rs` if applicable for building the aggregation query.
- Use `AppError` from `common/src/error.rs` with `.context()` wrapping for error handling.
- Implement the optional `threshold` parameter: when provided (e.g., "critical", "high", "medium", "low"), filter the counts to only include severities at or above the given threshold level. This filters the result fields, not the query — compute all counts, then zero out levels below the threshold.
- Per Error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust source file scope.
- Per Module pattern convention: each domain module follows model/ + service/ + endpoints/ structure. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Extend this existing service with the new method; follow its patterns for DB access and error handling
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference how advisory queries are structured for consistency
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; may be useful for structuring the aggregation query
- `common/src/error.rs::AppError` — Use the existing error type for 404 and other error responses
- `entity/src/sbom_advisory.rs` — The SBOM-Advisory join table entity needed for the aggregation query
- `entity/src/advisory.rs` — The Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService` has a `get_advisory_summary` method that returns `AdvisorySeveritySummary`
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns counts grouped by severity level (critical, high, medium, low) plus total
- [ ] Method returns 404-compatible error when SBOM ID does not exist
- [ ] Optional threshold parameter filters counts to only include severities at or above the given level
- [ ] Project compiles successfully

## Test Requirements
- [ ] Unit or integration test verifying correct severity counts for an SBOM with known advisories
- [ ] Test verifying deduplication: duplicate advisory-SBOM links produce correct counts
- [ ] Test verifying 404 error when querying a non-existent SBOM ID
- [ ] Test verifying threshold parameter filters counts correctly

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model

# Task 2 — Add severity aggregation service method to SbomService

## Repository
trustify-backend

## Target Branch
main

## Description
Add a method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` entity to retrieve severity, deduplicates by advisory ID, and aggregates counts by severity level (Critical, High, Medium, Low). This method returns an `AdvisorySeveritySummary` struct. It must also validate that the SBOM exists and return an appropriate error (404) if not found. This service method supports the non-functional requirement of p95 < 200ms for SBOMs with up to 500 advisories by performing the aggregation in a single database query rather than fetching all advisories and counting in application code.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn get_advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<String>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService: fetch, list, ingest`) for error handling and database access conventions.
- Use SeaORM to construct a query that:
  1. Verifies the SBOM exists (return 404 `AppError` if not found, consistent with existing SBOM endpoints)
  2. Joins `sbom_advisory` to `advisory` entity to access severity
  3. Uses `GROUP BY severity` with `COUNT(DISTINCT advisory_id)` to deduplicate and aggregate in a single SQL query
  4. Maps severity strings to the appropriate count fields in `AdvisorySeveritySummary`
- Reference `entity/sbom_advisory.rs` for the join table entity definition and `entity/advisory.rs` for the advisory entity with the severity field.
- Use `.context()` error wrapping as per `common/src/error.rs` (`AppError`) — this is the standard error handling pattern.
- The `threshold` parameter is optional and filters counts to only include severities at or above the given level (e.g., `threshold=high` returns only `critical` and `high` counts, with `medium` and `low` as 0). Severity ordering: Critical > High > Medium > Low.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — contains existing service methods (`fetch`, `list`, `ingest`) that demonstrate the database access pattern, error handling, and return type conventions
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; may contain reusable query construction utilities
- `common/src/error.rs::AppError` — the error enum that all service methods return; use `AppError::NotFound` for missing SBOMs
- `entity/sbom_advisory.rs` — the join table entity that links SBOMs to advisories; used to build the aggregation query
- `entity/advisory.rs` — advisory entity containing the severity field used for grouping

## Acceptance Criteria
- [ ] `SbomService` has a new `get_advisory_severity_summary` method
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for each severity level
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Optional `threshold` parameter correctly filters severity levels
- [ ] Aggregation is performed in a single database query (not application-side counting)

## Test Requirements
- [ ] Test that the method returns correct severity counts for an SBOM with known advisories at various severity levels
- [ ] Test deduplication: an advisory linked to an SBOM multiple times is counted only once
- [ ] Test 404 response when SBOM ID does not exist
- [ ] Test threshold filtering: `threshold=critical` returns only critical count, others zero
- [ ] Test threshold filtering: `threshold=high` returns critical and high counts, others zero
- [ ] Test empty result: SBOM exists but has no linked advisories returns all zeros

## Verification Commands
- `cargo build -p trustify-fundamental` — expected outcome: compiles without errors
- `cargo test -p trustify-fundamental` — expected outcome: service tests pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the advisory severity counts for a given SBOM ID. The method joins the `sbom_advisory` table with the `advisory` table, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary`. If the SBOM ID does not exist, the method returns an error that maps to HTTP 404.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest) for method signatures, error handling, and database query patterns.
- Use SeaORM query builder to join `sbom_advisory` with `advisory` entities, filtering by the given SBOM ID.
- Deduplicate by advisory ID before counting — use `DISTINCT` or `GROUP BY` on the advisory ID to ensure each advisory is counted only once even if linked multiple times.
- Group results by the `severity` field from the `advisory` entity (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for the severity field definition).
- Compute `total` as the sum of all severity counts.
- For SBOM existence check, first verify the SBOM exists (reuse the existing `fetch` method on `SbomService`). If not found, return an `AppError` that maps to 404, consistent with existing SBOM endpoint error handling in `common/src/error.rs`.
- Use shared query helpers from `common/src/db/query.rs` if applicable for filtering.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with database access patterns and error handling to follow
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the join query
- `entity/src/advisory.rs` — Advisory entity containing the severity field
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation for 404 mapping
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomService` has a new method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Query deduplicates advisories by advisory ID (each advisory counted once)
- [ ] Query groups by severity and returns correct counts for critical, high, medium, low
- [ ] Total field equals the sum of all severity counts
- [ ] Returns 404-mapped error when SBOM ID does not exist
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit/integration test: given an SBOM with known advisories at various severities, verify the returned counts match expected values
- [ ] Unit/integration test: given an SBOM with duplicate advisory links (same advisory linked multiple times), verify deduplication produces correct count
- [ ] Unit/integration test: given a non-existent SBOM ID, verify the method returns a 404-mapped error

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

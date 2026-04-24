# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Description
Add a new method to `SbomService` that aggregates advisory severity counts for a given SBOM ID. The method queries the existing `sbom_advisory` join table (entity `sbom_advisory.rs`) and the `advisory` entity to count unique advisories at each severity level (Critical, High, Medium, Low). It must deduplicate by advisory ID to avoid double-counting. The method returns an `AdvisorySeveritySummary` on success, or an appropriate error if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add the `get_advisory_summary` method to `SbomService`

## API Changes
- Internal service API: `SbomService::get_advisory_summary(sbom_id: Uuid, threshold: Option<String>) -> Result<AdvisorySeveritySummary, AppError>` — NEW

## Implementation Notes
- Follow the query patterns in `SbomService` at `modules/fundamental/src/sbom/service/sbom.rs` for database access via SeaORM.
- Use the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) to join SBOMs with advisories, and the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- The severity field type can be found on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — understand its enum or string representation to map to the four severity buckets (critical, high, medium, low).
- Deduplicate by advisory ID: use `SELECT DISTINCT advisory_id` or `GROUP BY advisory_id` in the query to ensure each advisory is counted only once even if linked multiple times.
- For the optional `threshold` parameter: when provided (e.g., `threshold=critical`), only count advisories at or above the specified severity. The severity ordering is: critical > high > medium > low. This is a non-MVP feature but should be designed into the method signature now.
- First verify the SBOM exists by querying the `sbom` entity (`entity/src/sbom.rs`). Return `AppError::NotFound` (from `common/src/error.rs`) if not found — consistent with existing SBOM endpoints like `GET /api/v2/sbom/{id}` in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Use the shared query helpers from `common/src/db/query.rs` if applicable for building the aggregation query.
- The query should be efficient for SBOMs with up to 500 advisories (p95 < 200ms target). A single SQL aggregation query with `COUNT` and `CASE WHEN` (or `GROUP BY severity`) is preferred over fetching all advisories and counting in Rust.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct; add the new method here following its patterns for DB access and error handling
- `common/src/error.rs::AppError` — use `AppError::NotFound` for missing SBOM, matching the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`
- `common/src/db/query.rs` — shared query builder helpers that may assist with building the aggregation query
- `entity/src/sbom_advisory.rs` — the join table entity connecting SBOMs to advisories
- `entity/src/advisory.rs` — advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method is implemented and compiles
- [ ] Method returns correct severity counts (critical, high, medium, low, total) for a given SBOM
- [ ] Advisories are deduplicated by advisory ID (no double-counting)
- [ ] Returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Optional `threshold` parameter filters counts to only include severities at or above the specified level
- [ ] Single SQL query is used for aggregation (no N+1 or client-side counting)

## Test Requirements
- [ ] Service test: returns correct severity counts for an SBOM with advisories at multiple severity levels
- [ ] Service test: deduplicates advisories linked to the same SBOM multiple times
- [ ] Service test: returns `NotFound` error for a non-existent SBOM ID
- [ ] Service test: threshold filtering correctly includes only severities at or above the threshold
- [ ] Service test: returns all-zero counts for an SBOM with no linked advisories

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — service tests should pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

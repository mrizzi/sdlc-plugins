# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Description
Add a new method to `SbomService` that queries and aggregates advisory severity counts for a given SBOM ID. The method must deduplicate advisories by advisory ID (since an advisory can be linked to an SBOM through multiple paths), count by severity level, and return an `AdvisorySeveritySummary`. It must also return an appropriate error when the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add the aggregation method to `SbomService`

## Implementation Notes
- Use the existing `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`) to find advisories linked to a given SBOM.
- Use the `advisory` entity (`entity/src/advisory.rs`) to access the severity field for each linked advisory.
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT` or `GROUP BY` in the SeaORM query to avoid double-counting advisories linked through multiple vulnerability paths.
- The aggregation query should count advisories per severity level. Prefer a single database query with `GROUP BY severity` over multiple queries or fetching all records into memory.
- Follow the error handling pattern in existing `SbomService` methods (`modules/fundamental/src/sbom/service/sbom.rs`): return `Result<T, AppError>` and use `.context()` for error wrapping, consistent with `common/src/error.rs::AppError`.
- For the SBOM existence check, follow the pattern used by `GET /api/v2/sbom/{id}` in `modules/fundamental/src/sbom/endpoints/get.rs` — if no SBOM is found, return an error that maps to HTTP 404.
- Support an optional severity threshold parameter: when provided (e.g., `"critical"`), only return counts for severities at or above the threshold. Severity ordering: Critical > High > Medium > Low.
- Per constraints doc section 5.4: do not duplicate existing query patterns. Reuse `common/src/db/query.rs` helpers for filtering if applicable.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods demonstrate the query pattern, database connection usage, and error handling conventions
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — may contain existing query patterns for filtering advisories by severity
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity needed for the aggregation query
- `entity/src/advisory.rs` — the advisory entity containing the severity field
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type and IntoResponse implementation

## Acceptance Criteria
- [ ] New method on `SbomService` returns `AdvisorySeveritySummary` with correct counts for critical, high, medium, and low severities
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Returns an error mapping to 404 when the SBOM ID does not exist
- [ ] Supports optional severity threshold filtering
- [ ] Uses a single efficient database query (not N+1)
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit/integration test verifying correct severity counts for an SBOM with known advisory data
- [ ] Test verifying deduplication: an advisory linked to an SBOM through multiple paths is counted only once
- [ ] Test verifying 404 error when querying a non-existent SBOM ID
- [ ] Test verifying threshold filtering returns only counts at or above the specified severity

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental sbom_service` — service tests should pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

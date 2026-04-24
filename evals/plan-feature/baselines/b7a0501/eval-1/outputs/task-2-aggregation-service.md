## Repository
trustify-backend

## Description
Implement the advisory severity aggregation service method that queries the `sbom_advisory` join table, deduplicates advisories by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary` with the counted totals. This method encapsulates the core business logic for the feature and is called by the endpoint handler (Task 3). The method must also validate that the requested SBOM exists and return an appropriate error if not found.

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — Service method `advisory_severity_summary(sbom_id)` that queries `sbom_advisory` joined with `advisory`, deduplicates by advisory ID, groups by severity, and returns `Result<AdvisorySeveritySummary, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` to expose the new service module

## Implementation Notes
- Follow the pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for service method structure, database connection handling, and error propagation with `.context()`.
- The query should join `entity/src/sbom_advisory.rs` with `entity/src/advisory.rs` to access the severity field on each advisory.
- Deduplicate by advisory ID before counting — the same advisory may appear multiple times in the join table if linked via different vulnerability paths. Use `SELECT DISTINCT advisory_id, severity` or equivalent SeaORM query.
- Group results by severity and count each group. Map severity values to the four levels (Critical, High, Medium, Low) and compute `total` as the sum.
- Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist, consistent with `modules/fundamental/src/sbom/endpoints/get.rs` which returns 404 for missing SBOMs.
- Use `common/src/db/query.rs` helpers if applicable for query construction.
- Target p95 < 200ms for SBOMs with up to 500 advisories — the query should leverage database-side aggregation (COUNT + GROUP BY) rather than fetching all rows and counting in Rust.
- Per constraints (section 5.4), do not duplicate existing query patterns — reuse query builder helpers from `common/src/db/query.rs` where applicable.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Pattern for service method signatures, database connection usage, and error handling
- `common/src/db/query.rs` — Shared query builder helpers for filtering and query construction
- `common/src/error.rs::AppError` — Error enum for 404 (NotFound) and other error responses
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity definition; primary table for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field used for grouping

## Acceptance Criteria
- [ ] Service method `advisory_severity_summary` exists and accepts an SBOM ID parameter
- [ ] Method queries `sbom_advisory` joined with `advisory`, deduplicates by advisory ID, and groups by severity
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for critical, high, medium, low, and total
- [ ] Method returns `AppError::NotFound` (404) when the SBOM ID does not exist
- [ ] Aggregation is performed database-side (COUNT + GROUP BY) not in application code
- [ ] Module is publicly exported from `modules/fundamental/src/sbom/service/mod.rs`
- [ ] `cargo check -p trustify-module-fundamental` compiles with no errors

## Test Requirements
- [ ] Unit test with a mock database context verifying correct severity counts for a known set of advisories
- [ ] Unit test verifying deduplication — same advisory linked twice returns count of 1
- [ ] Unit test verifying 404 error when SBOM ID does not exist
- [ ] Unit test verifying an SBOM with zero advisories returns all-zero counts (Default)

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — all unit tests pass

## Dependencies
- Depends on: Task 1 — Advisory summary model

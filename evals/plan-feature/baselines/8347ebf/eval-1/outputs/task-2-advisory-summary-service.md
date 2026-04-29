# Task 2 — Add Advisory Summary Service Method to SbomService

## Repository
trustify-backend

## Description
Add an `advisory_summary` method to `SbomService` that queries the `sbom_advisory` join table for a given SBOM ID, deduplicates advisories by advisory ID, groups them by severity level, and returns an `AdvisorySeveritySummary` with the counts. This server-side aggregation replaces the current client-side approach of fetching all advisories and counting by severity, reducing response time from ~2s to <200ms.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_summary` method to `SbomService`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService: fetch, list, ingest`).
- The method should accept a database connection/transaction and an SBOM ID parameter.
- Query the `sbom_advisory` join table defined in `entity/src/sbom_advisory.rs` to find all advisories linked to the given SBOM.
- Join with the advisory entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting — the same advisory may be linked multiple times.
- Group by severity level and count occurrences for each level (Critical, High, Medium, Low).
- Return `Result<AdvisorySeveritySummary, AppError>` using the error type from `common/src/error.rs`.
- Return a 404 error if the SBOM ID does not exist, consistent with existing SBOM endpoint behavior. Use `.context()` wrapping as per project conventions.
- Use SeaORM query builder patterns consistent with `common/src/db/query.rs` for shared query helpers.
- Performance requirement: p95 < 200ms for SBOMs with up to 500 advisories. Use a single aggregation query rather than fetching all rows and counting in Rust.
- Per `docs/constraints.md` §5.2: inspect code before modifying — read `SbomService` implementation before adding the method.
- Per `docs/constraints.md` §5.4: do not duplicate existing functionality; reuse query helpers from `common/src/db/query.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — the service struct to extend; follow its method signatures, error handling, and database access patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference its query patterns for advisory-related data access
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting); may contain reusable patterns for aggregation
- `common/src/error.rs::AppError` — error type for wrapping database and not-found errors

## Acceptance Criteria
- [ ] `advisory_summary` method exists on `SbomService`
- [ ] Method queries `sbom_advisory` join table and joins with `advisory` entity
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Severity counts are grouped correctly into Critical, High, Medium, Low
- [ ] `total` field equals the sum of all severity counts
- [ ] Returns 404 `AppError` when the SBOM ID does not exist
- [ ] Query executes as a single database aggregation (not fetch-all-then-count)

## Test Requirements
- [ ] Unit test: service returns correct severity counts for an SBOM with known advisory distribution
- [ ] Unit test: service returns all-zero counts for an SBOM with no linked advisories
- [ ] Unit test: service deduplicates advisories that are linked multiple times
- [ ] Unit test: service returns 404 error for a nonexistent SBOM ID

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary Response Model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation query method to `SbomService` that counts unique advisories by severity level for a given SBOM ID. This method queries the existing `sbom_advisory` join table to count advisories grouped by severity, deduplicating by advisory ID. It returns a `SeveritySummary` struct. If the SBOM ID does not exist, the method returns an appropriate error that the endpoint layer can map to a 404 response.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_summary` method to `SbomService`

## Implementation Notes
Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods for fetch, list, ingest). Each service method accepts a database connection/transaction parameter and returns `Result<T, AppError>`.

The query should:
1. Verify the SBOM exists (return `AppError` not-found if missing)
2. Join `sbom_advisory` with `advisory` entities to access the severity field
3. Use `GROUP BY` on the severity column and `COUNT(DISTINCT advisory_id)` to deduplicate
4. Map the grouped results into a `SeveritySummary` struct

Use the SeaORM query builder patterns from `common/src/db/query.rs` for constructing the aggregation query. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` shows how the severity field is defined on advisories.

Entity definitions in `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) and `entity/src/advisory.rs` (Advisory entity with severity field) provide the schema for this query.

Per CONVENTIONS.md §Error handling: return `Result<SeveritySummary, AppError>` and use `.context()` wrapping on database errors.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering and query builder helpers from `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct; add the new method following established patterns for database queries and error handling
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse for constructing the aggregation query
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for the join query
- `entity/src/advisory.rs` — Advisory entity with severity field; use for grouping by severity
- `common/src/error.rs::AppError` — Error enum with `IntoResponse` implementation; use for not-found and database error cases

## Acceptance Criteria
- [ ] `SbomService` has a `get_advisory_summary` method that returns `Result<SeveritySummary, AppError>`
- [ ] Method returns advisory counts grouped by severity (critical, high, medium, low) with a total
- [ ] Advisories are deduplicated by advisory ID (unique count)
- [ ] Method returns a not-found error when the SBOM ID does not exist
- [ ] No new database tables are created — uses existing `sbom_advisory` and `advisory` tables

## Test Requirements
- [ ] Unit test verifying correct aggregation with multiple advisories at different severity levels
- [ ] Unit test verifying deduplication (same advisory linked twice returns count of 1)
- [ ] Unit test verifying not-found error for non-existent SBOM ID

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors

## Dependencies
- Depends on: Task 1 — Add SeveritySummary model struct

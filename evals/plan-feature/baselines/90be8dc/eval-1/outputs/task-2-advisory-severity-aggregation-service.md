## Repository
trustify-backend

## Description
Implement a service method that queries the database to aggregate advisory severity counts for a given SBOM. The method joins the `sbom_advisory` table with the `advisory` table, groups by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists and returns an appropriate error if not found.

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — New service module containing the `get_advisory_severity_summary` method that performs the aggregation query

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` declaration to expose the new service module

## Implementation Notes
Add the aggregation method to the existing `SbomService` via an `impl` block in the new module file, following the pattern in `modules/fundamental/src/sbom/service/sbom.rs`. The method should:

1. First verify the SBOM exists by querying `entity/src/sbom.rs` entity -- return `AppError` with 404 status if not found, following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
2. Query using SeaORM: join `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) with `entity/src/advisory.rs` (Advisory entity) on advisory ID.
3. Use `SELECT COUNT(DISTINCT advisory.id), advisory.severity` with `GROUP BY advisory.severity` to deduplicate advisories and count per severity level.
4. Map the query results into an `AdvisorySeveritySummary` struct, defaulting missing severity levels to 0.
5. Compute `total` as the sum of all severity counts.

Use `common/src/db/query.rs` query builder helpers for constructing the query. Wrap all database errors with `.context()` as per the error handling convention using `common/src/error.rs::AppError`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Extend this service with the new aggregation method
- `entity/src/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join table, use for the aggregation join
- `entity/src/advisory.rs` — Advisory entity with severity column to group by
- `common/src/db/query.rs` — Query builder helpers for filtering and constructing queries
- `common/src/error.rs::AppError` — Error type for 404 and internal errors

## Acceptance Criteria
- [ ] `get_advisory_severity_summary(sbom_id)` method exists on `SbomService`
- [ ] Method returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Advisory IDs are deduplicated before counting (no double-counting)
- [ ] Returns 404 error when SBOM ID does not exist
- [ ] All four severity levels (critical, high, medium, low) are counted correctly
- [ ] `total` field equals the sum of all severity counts

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors

## Dependencies
- Depends on: Task 1 — Define AdvisorySeveritySummary response model

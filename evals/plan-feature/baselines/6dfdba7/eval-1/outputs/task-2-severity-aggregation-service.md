## Repository
trustify-backend

## Description
Implement the service-layer method that queries the database to aggregate advisory severity counts for a given SBOM. This method joins the `sbom_advisory` table with the `advisory` table, groups by severity level, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. It also supports an optional severity threshold filter that excludes severities below the specified level. This is the core business logic for TC-9001.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<String>, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing query patterns in `SbomService` within `modules/fundamental/src/sbom/service/sbom.rs`. Existing methods like `fetch` likely take a database connection and return `Result<T, AppError>`.
- Use SeaORM query builder to construct the aggregation query. The query should:
  1. Select from `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) filtered by the given `sbom_id`
  2. Join `advisory` entity (`entity/src/advisory.rs`) to access the severity column
  3. Use `SELECT COUNT(DISTINCT advisory.id)` grouped by `advisory.severity` to deduplicate
  4. Map the grouped counts into the `AdvisorySeveritySummary` struct
- For the threshold filter: define a severity ordering (Critical > High > Medium > Low), and when `threshold` is provided, only include severities at or above that level. Counts for excluded severities should be 0.
- Use the `AppError` enum from `common/src/error.rs` for error handling. Return a 404-equivalent error if the SBOM ID does not exist (check existence first with an SBOM lookup, consistent with existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/get.rs`).
- Query helpers in `common/src/db/query.rs` may be useful for filtering, but the aggregation is custom enough to require a direct SeaORM query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct to extend; follow its method signatures and error handling patterns
- `common/src/error.rs::AppError` — Error type for 404 and internal errors
- `common/src/db/query.rs` — Query builder helpers for filtering
- `entity/src/sbom_advisory.rs` — Join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with the severity column

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary` method exists and compiles
- [ ] Method queries `sbom_advisory` joined with `advisory`, grouping by severity
- [ ] Advisory IDs are deduplicated (COUNT DISTINCT)
- [ ] Returns `AdvisorySeveritySummary` with correct counts
- [ ] Returns appropriate error when SBOM ID does not exist
- [ ] Optional `threshold` parameter filters out severities below the threshold
- [ ] Total field equals sum of included severity counts

## Test Requirements
- [ ] Unit test: method returns correct counts for an SBOM with known advisories at multiple severity levels
- [ ] Unit test: method returns all zeros for an SBOM with no linked advisories
- [ ] Unit test: method returns 404-equivalent error for a non-existent SBOM ID
- [ ] Unit test: threshold filter correctly excludes lower severities

## Verification Commands
- `cargo check -p trustify-fundamental` — should compile without errors

## Dependencies
- Depends on: Task 1 — Advisory summary model (provides `AdvisorySeveritySummary` struct)

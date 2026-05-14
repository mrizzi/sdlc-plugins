## Repository
trustify-backend

## Target Branch
main

## Description
Add a `get_advisory_severity_summary` method to `SbomService` that queries the database for advisory severity counts associated with a given SBOM. The method performs a SQL aggregation query joining `sbom_advisory` with `advisory`, grouping by severity, deduplicating by advisory ID, and returning an `AdvisorySeveritySummary`. It must also verify SBOM existence and return an appropriate error for missing SBOMs.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `pub async fn get_advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<String>, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`. This method queries the `sbom_advisory` join table joined with the `advisory` table to get severity counts.
- `modules/fundamental/src/sbom/service/mod.rs` — Add any necessary imports or re-exports for the new method's return type.

## Implementation Notes
- Follow the query pattern in `modules/fundamental/src/sbom/service/sbom.rs` for existing `SbomService` methods (fetch, list, ingest). Use the same `DatabaseConnection` parameter style and error handling with `AppError` and `.context()` wrapping from `common/src/error.rs`.
- Use SeaORM's `Entity::find()` and join API to query `entity::sbom_advisory::Entity` joined with `entity::advisory::Entity`. The severity field is on the `advisory` entity (`entity/src/advisory.rs`).
- First check SBOM existence by querying `entity::sbom::Entity::find_by_id(sbom_id)`. Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM does not exist.
- Use `SELECT advisory.severity, COUNT(DISTINCT advisory.id)` semantics to deduplicate advisories. SeaORM's `Column::count_distinct()` or a raw query builder from `common/src/db/query.rs` can achieve this.
- Map the severity strings (e.g., "critical", "high", "medium", "low") from the query results into the corresponding `AdvisorySeveritySummary` fields. Handle unknown severity values gracefully (ignore or log).
- If `threshold` is `Some("critical")`, only include advisories with severity >= critical. Implement this as a WHERE clause filter on the severity column. Support values: "critical" (only critical), "high" (critical + high), "medium" (critical + high + medium), "low" (all — same as no filter).
- The `total` field in the response should be the sum of the included severity counts.

## Acceptance Criteria
- [ ] `SbomService::get_advisory_severity_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for each severity level
- [ ] Method returns `AppError::NotFound` (404-equivalent) when the SBOM ID does not exist
- [ ] Advisories are deduplicated by advisory ID (each advisory counted once regardless of how many times it is linked)
- [ ] Optional `threshold` parameter filters severity levels correctly
- [ ] `total` field equals the sum of the included severity counts

## Test Requirements
- [ ] Unit/integration test: given an SBOM with known advisories at each severity level, verify the returned counts match expected values
- [ ] Unit/integration test: query for a non-existent SBOM ID returns a not-found error
- [ ] Unit/integration test: verify deduplication — same advisory linked multiple times to the same SBOM is counted once
- [ ] Unit/integration test: verify threshold filtering returns only counts at or above the specified severity

## Dependencies
- Depends on: Task 1 — Advisory summary model (provides `AdvisorySeveritySummary` struct)

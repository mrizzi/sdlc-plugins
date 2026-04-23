## Repository
trustify-backend

## Description
Implement the advisory severity aggregation query in `SbomService`. This method will query the `sbom_advisory` join table, join to the `advisory` table to retrieve severity, group by severity level, and return deduplicated counts as an `AdvisorySeveritySummary`. The method must also verify that the SBOM exists and return an appropriate error if not found.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add a new `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Add the method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the pattern of existing methods like `fetch` and `list` that accept an ID and return a result.
- Use SeaORM to query the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Apply `GROUP BY severity` and `COUNT(DISTINCT advisory_id)` to deduplicate advisories by ID as required by the feature spec.
- Filter by the given `sbom_id` using the SBOM foreign key on the `sbom_advisory` join table.
- Before aggregating, verify the SBOM exists by calling the existing `fetch` method or querying the `sbom` entity (`entity/src/sbom.rs`) directly. If not found, return `AppError::NotFound` consistent with `common/src/error.rs`.
- Map the query result rows into severity buckets (critical, high, medium, low) and compute the total as the sum of all buckets.
- Use the query builder helpers from `common/src/db/query.rs` if applicable for filtering.

## Reuse Candidates
- `common/src/error.rs::AppError` — Use `AppError::NotFound` for missing SBOM, consistent with other service methods
- `common/src/db/query.rs` — Shared query builder helpers for filtering
- `entity/src/sbom_advisory.rs` — The join table entity that links SBOMs to advisories
- `entity/src/advisory.rs` — Advisory entity containing the severity field
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — Pattern for ID-based lookup and not-found handling

## Acceptance Criteria
- [ ] `SbomService` has a new `advisory_severity_summary` method that accepts an SBOM ID
- [ ] Method returns `AdvisorySeveritySummary` with correct counts grouped by severity
- [ ] Advisories are deduplicated by advisory ID (COUNT DISTINCT)
- [ ] Method returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Method computes `total` as the sum of all severity counts

## Test Requirements
- [ ] Unit/integration test: returns correct severity counts for an SBOM with known advisories at each severity level
- [ ] Unit/integration test: returns all-zero counts for an SBOM with no linked advisories
- [ ] Unit/integration test: returns `NotFound` error for a non-existent SBOM ID
- [ ] Unit/integration test: deduplicates advisories that appear multiple times in the join table

## Dependencies
- Depends on: Task 1 — Advisory summary model (requires `AdvisorySeveritySummary` struct)

## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation method to `SbomService` that queries the database for advisory severity counts associated with a given SBOM ID. The method groups advisories by severity level, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary` with counts for critical, high, medium, and low severities plus a total.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Use SeaORM query builder to join `entity::sbom_advisory` (from `entity/src/sbom_advisory.rs`) with `entity::advisory` (from `entity/src/advisory.rs`) to access the severity field on each advisory.
- Group results by severity and count distinct advisory IDs to deduplicate advisories that may be linked to the same SBOM multiple times.
- Reference existing query patterns in `common/src/db/query.rs` for building filtered queries with SeaORM.
- Use the `entity::sbom::Entity::find_by_id(sbom_id)` pattern already present in `modules/fundamental/src/sbom/service/sbom.rs` to verify SBOM existence before aggregating; return `AppError::NotFound` if the SBOM does not exist.
- Compute the `total` field as the sum of all severity counts.
- Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context() wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust language scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Standard error type for propagating database and not-found errors
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct to extend with the new aggregation method

## Acceptance Criteria
- [ ] `get_advisory_summary` method added to `SbomService`
- [ ] Returns correct counts grouped by severity (critical, high, medium, low, total)
- [ ] Deduplicates advisories by advisory ID before counting
- [ ] Returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Total field equals the sum of all severity counts

## Test Requirements
- [ ] Correct aggregation with multiple advisories at different severities
- [ ] Deduplication when same advisory is linked to SBOM multiple times
- [ ] Returns not-found error when SBOM ID does not exist
- [ ] Returns all-zero counts when SBOM exists but has no linked advisories

## Dependencies
- Depends on: Task 1 — Define AdvisorySeveritySummary response model

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira

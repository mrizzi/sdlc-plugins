# Task 2 — Add severity aggregation query to AdvisoryService

## Repository
trustify-backend

## Description
Add a method to `AdvisoryService` that queries the database to count unique advisories per severity level for a given SBOM ID. This method performs a SQL aggregation over the `sbom_advisory` join table joined with the `advisory` table, grouping by severity and deduplicating by advisory ID, returning an `AdvisorySeveritySummary`.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add `get_severity_summary_for_sbom(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `AdvisoryService`

## API Changes
- `AdvisoryService::get_severity_summary_for_sbom(sbom_id)` — NEW: aggregates advisory severity counts for a given SBOM

## Implementation Notes
- Follow the query pattern established in `AdvisoryService` at `modules/fundamental/src/advisory/service/advisory.rs` — existing methods use SeaORM `Entity::find()` with filters and joins.
- Use the `sbom_advisory` join entity at `entity/src/sbom_advisory.rs` to join advisories to the target SBOM.
- Use the `advisory` entity at `entity/src/advisory.rs` to access the severity field.
- The query must `COUNT(DISTINCT advisory.id)` grouped by severity to handle deduplication as required by the feature specification.
- Use `common/src/db/query.rs` for any shared query helper patterns (filtering, etc.).
- Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist — first verify the SBOM exists by querying the `sbom` entity at `entity/src/sbom.rs`.
- Support an optional `threshold` parameter: when provided, only return counts for severities at or above the threshold (Critical > High > Medium > Low).
- Per constraints §5.2: inspect `AdvisoryService` existing methods before implementing to match established patterns.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service with fetch/list/search methods to follow as patterns
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity needed for the aggregation join
- `entity/src/advisory.rs` — Advisory entity with severity field
- `common/src/error.rs::AppError` — error type for 404 handling
- `common/src/db/query.rs` — shared query builder helpers

## Acceptance Criteria
- [ ] `AdvisoryService` has a `get_severity_summary_for_sbom` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method counts unique advisories (deduplicated by advisory ID) grouped by severity
- [ ] Returns `AppError::NotFound` if the SBOM ID does not exist
- [ ] Supports optional threshold filtering (only counts at or above the specified severity)

## Test Requirements
- [ ] Unit test with a known dataset verifying correct severity counts are returned
- [ ] Unit test verifying deduplication — same advisory linked to SBOM multiple times is counted once
- [ ] Unit test verifying `AppError::NotFound` is returned for a non-existent SBOM ID
- [ ] Unit test verifying threshold filtering returns only severities at or above the threshold

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

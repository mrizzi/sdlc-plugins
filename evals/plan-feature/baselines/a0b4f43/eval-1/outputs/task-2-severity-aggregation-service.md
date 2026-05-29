## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the database for all advisories linked to a given SBOM, deduplicates them by advisory ID, groups them by severity level, and returns an `AdvisorySeveritySummary` with the counts. This method forms the core business logic for the advisory severity aggregation feature. The query must use the existing `sbom_advisory` join table entity and the `advisory` entity to resolve severity values without creating new database tables.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the query pattern in `modules/fundamental/src/sbom/service/sbom.rs` for existing `SbomService` methods (fetch, list, ingest). These methods demonstrate the database query conventions, error handling with `.context()`, and return type patterns.
- Use SeaORM to join `sbom_advisory` (from `entity/src/sbom_advisory.rs`) with `advisory` (from `entity/src/advisory.rs`) to resolve severity values for each linked advisory.
- Deduplicate by advisory ID using `SELECT DISTINCT` or equivalent SeaORM operation to ensure each advisory is counted only once even if linked multiple times.
- Group results by severity and count occurrences for each level (critical, high, medium, low).
- Return 404 (`AppError::NotFound`) if the SBOM ID does not exist. Check the `common/src/error.rs` `AppError` enum for the existing error variant pattern.
- Use the shared query helpers from `common/src/db/query.rs` where applicable for consistent query building.
- Per docs/constraints.md section 2 (Commit Rules): commit must reference Jira issue ID in footer and follow Conventional Commits format.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code before modifying (constraint 5.2), follow patterns in Implementation Notes (constraint 5.3), do not duplicate existing functionality (constraint 5.4).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Contains the existing service methods demonstrating the query pattern, error handling, and database connection usage
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Shows how advisory entities are queried and severity fields are accessed
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting
- `common/src/error.rs::AppError` — Error enum with existing variants for NotFound and other error cases
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity used for the relationship query

## Acceptance Criteria
- [ ] `SbomService` has a new method `advisory_severity_summary` that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method queries the `sbom_advisory` join table joined with `advisory` to retrieve severity data
- [ ] Advisory deduplication by advisory ID is implemented to prevent double-counting
- [ ] Severity counts are correctly aggregated into critical, high, medium, low, and total fields
- [ ] Returns 404 error when the SBOM ID does not exist in the database
- [ ] Code compiles and passes existing tests without regression

## Test Requirements
- [ ] Unit test: service returns correct severity counts for an SBOM with multiple advisories at different severity levels
- [ ] Unit test: service deduplicates advisories that are linked to the same SBOM multiple times
- [ ] Unit test: service returns all zeros when an SBOM has no linked advisories
- [ ] Unit test: service returns 404 when given a non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model struct

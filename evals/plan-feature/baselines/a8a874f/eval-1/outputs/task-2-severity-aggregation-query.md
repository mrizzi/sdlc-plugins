# Task 2: Add severity aggregation query to SbomService

## Repository

trustify-backend

## Target Branch

main

## Dependencies

- Task 1 (advisory severity summary model)

## Description

Implement a method on `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM ID. This method queries the `sbom_advisory` join table joined with the `advisory` table, groups by severity, counts unique advisory IDs, and returns an `AdvisorySeveritySummary`. The method must return a 404-equivalent error if the SBOM ID does not exist, consistent with other SBOM service methods.

## Files to Modify

- `modules/fundamental/src/sbom/service/sbom.rs` -- add `pub async fn advisory_severity_summary(&self, sbom_id: Uuid, db: &DbConn) -> Result<AdvisorySeveritySummary, AppError>` method

## Implementation Notes

- Follow the query patterns in `modules/fundamental/src/sbom/service/sbom.rs` (the existing `SbomService` methods for `fetch` and `list`). Service methods accept a database connection and return `Result<T, AppError>`.
- Use SeaORM to query: join `entity::sbom_advisory` with `entity::advisory` on advisory ID, filter by `sbom_id`, select severity and `COUNT(DISTINCT advisory_id)`, group by severity.
- Reference `entity/src/sbom_advisory.rs` for the join table schema and `entity/src/advisory.rs` for the advisory entity (which has the severity column).
- First check that the SBOM exists by querying `entity::sbom` -- if not found, return an `AppError` 404 error following the pattern in `common/src/error.rs`.
- Deduplicate by advisory ID (use `COUNT(DISTINCT ...)` or equivalent) as required by the feature spec.
- Map the grouped severity counts to the `AdvisorySeveritySummary` struct fields. Severities not present in the result set should default to 0.
- Use `common/src/db/query.rs` helpers if applicable for query construction.

### Applicable Conventions

- **Error handling**: Applies: task modifies `sbom.rs` matching the convention's Rust service file scope -- all handlers return `Result<T, AppError>` with `.context()` wrapping.

## Acceptance Criteria

- [ ] `SbomService::advisory_severity_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct counts grouped by severity
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Severities not present in the database default to 0 in the response

## Test Requirements

- [ ] Integration test: SBOM with advisories at multiple severity levels returns correct counts
- [ ] Integration test: SBOM with no advisories returns all zeros with total=0
- [ ] Integration test: non-existent SBOM ID returns 404 error
- [ ] Integration test: duplicate advisory-SBOM links produce deduplicated counts

[Description digest: sha256-md:b4e8c3d2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4 would be posted as a comment]

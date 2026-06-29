## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer method that queries the database to aggregate advisory severity counts for a given SBOM ID. This method joins the `sbom_advisory` and `advisory` tables, groups by severity, counts distinct advisory IDs, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists (returning an error if not found) and supports optional threshold filtering.

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — `fetch_advisory_summary` method on `SbomService` (or as a standalone function) that takes a database connection, SBOM ID, and optional `SeverityThreshold`, and returns `Result<AdvisorySeveritySummary, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod advisory_summary;` to expose the new service module

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` defines methods for fetch and list operations. The new method should:

1. Query `entity::sbom` to verify the SBOM ID exists; if not, return `AppError::NotFound` (see error patterns in `common/src/error.rs`).
2. Join `entity::sbom_advisory` with `entity::advisory` on advisory ID.
3. Filter by the given SBOM ID.
4. Use `SELECT COUNT(DISTINCT advisory_id)` grouped by severity to deduplicate advisories.
5. Map the severity groupings into the `AdvisorySeveritySummary` struct fields.
6. If a `SeverityThreshold` is provided, zero out severity levels below the threshold.
7. Compute the `total` field as the sum of all non-zeroed severity counts.

Reference `common/src/db/query.rs` for shared query builder helpers that may be reusable for filtering. Reference `entity/src/sbom_advisory.rs` for the join table entity structure and `entity/src/advisory.rs` for the severity column.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and use `.context()` wrapping on database errors.
Applies: task creates `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: create the service file under `service/` following the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for filtering operations.
Applies: task creates `modules/fundamental/src/sbom/service/advisory_summary.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — error type for not-found and database error cases
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `entity/src/sbom_advisory.rs` — join table entity for SBOM-to-advisory relationship
- `entity/src/advisory.rs` — advisory entity with severity field
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern to follow

## Acceptance Criteria
- [ ] Service method queries `sbom_advisory` joined with `advisory` for the given SBOM ID
- [ ] Advisory counts are deduplicated by advisory ID
- [ ] Counts are grouped by severity level into `AdvisorySeveritySummary` fields
- [ ] Returns `AppError` (404 equivalent) when SBOM ID does not exist
- [ ] Optional threshold parameter filters out severity levels below the threshold
- [ ] Total field equals the sum of all included severity counts
- [ ] Method uses `.context()` wrapping for database errors

## Test Requirements
- [ ] Unit test verifying correct aggregation with mock data across multiple severity levels
- [ ] Unit test verifying 404 error is returned for non-existent SBOM ID
- [ ] Unit test verifying threshold filtering zeroes out appropriate severity levels
- [ ] Unit test verifying deduplication of advisories with the same ID

## Dependencies
- Depends on: Task 1 — Advisory summary model (provides `AdvisorySeveritySummary` and `SeverityThreshold` types)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:6a189fa65b08e3d112361b4edd9ccb9a3a70648f89c16e3abeb6d27be0c36dcf

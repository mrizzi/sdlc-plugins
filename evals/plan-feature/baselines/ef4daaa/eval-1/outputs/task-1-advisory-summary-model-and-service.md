# Task 1 — Add advisory severity summary model and service method

## Repository
trustify-backend

## Description
Add a response model struct for the advisory severity summary and a service method that computes deduplicated severity counts for a given SBOM. This provides the data layer that the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint will expose. The service method queries the existing `sbom_advisory` join table, joins with the `advisory` table to access severity, deduplicates by advisory ID, groups by severity level (Critical, High, Medium, Low), and returns the counts along with a total.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `AdvisorySeveritySummary` model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — re-export the new service method if needed

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }` (this task implements the model and service layer; the endpoint is wired in Task 2)

## Implementation Notes
- Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). The new `AdvisorySeveritySummary` struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema` like sibling model structs.
- The struct fields should be: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- The service method should be added to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the pattern of existing methods like `fetch` and `list`.
- Use SeaORM queries against the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT advisory_id, severity FROM sbom_advisory JOIN advisory ...` or equivalent SeaORM query.
- The severity field is available on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`), which confirms the advisory entity has a severity column.
- Use the shared query helpers from `common/src/db/query.rs` if applicable for building the query.
- Return `Result<AdvisorySeveritySummary, AppError>` following the error handling pattern in `common/src/error.rs`. Return a 404 `AppError` variant if the SBOM ID does not exist.
- Per the feature requirements: "No new database tables" — only use existing `sbom_advisory` and `advisory` tables.
- Per constraints doc section 5.2: Code MUST NOT be modified without first inspecting it. The implementer should read the existing `SbomService` methods and SeaORM entity definitions before writing the query.
- Per constraints doc section 5.4: Code MUST NOT duplicate existing functionality. Check if `AdvisoryService` already has severity-related helpers that can be reused.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the new method; follow its query patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reference for valid severity values
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity; use for the aggregation query
- `entity/src/advisory.rs` — the Advisory entity with severity column
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for 404 and other error responses

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] `SbomService` has an `advisory_severity_summary` method that takes an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The service method deduplicates advisories by advisory ID before counting
- [ ] The service method returns 404 if the SBOM ID does not exist
- [ ] The model struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test that the service method returns correct severity counts for an SBOM with known advisories at each severity level
- [ ] Unit test that the service method deduplicates advisories (same advisory linked multiple times is counted once)
- [ ] Unit test that the service method returns 404 for a non-existent SBOM ID
- [ ] Unit test that the service method returns all-zero counts for an SBOM with no linked advisories

## Dependencies
- None (this is the foundation task)

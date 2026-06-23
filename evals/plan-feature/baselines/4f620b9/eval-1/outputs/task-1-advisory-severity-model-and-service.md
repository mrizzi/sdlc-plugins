## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` model struct and a service method on `SbomService` that queries the `sbom_advisory` join table to aggregate advisory counts by severity level (critical, high, medium, low). The service method deduplicates advisories by advisory ID before counting and returns a total count. This provides the data layer for the new advisory summary endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `AdvisorySeveritySummary` struct
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — define the `AdvisorySeveritySummary` response struct with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct definition conventions (derive macros, serde attributes).
- The `AdvisorySeveritySummary` struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug` at minimum, consistent with sibling model structs.
- The service method `get_advisory_severity_summary(sbom_id)` should be added to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the pattern of existing methods like `fetch` and `list`.
- Use the `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`) to query advisories linked to the given SBOM.
- Use the `advisory` entity (`entity/src/advisory.rs`) to access the severity field from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT` or equivalent SeaORM query to avoid double-counting advisories linked through multiple paths.
- Return `Result<AdvisorySeveritySummary, AppError>` following the error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping.
- The method should return a 404-equivalent error (propagated as `AppError`) if the SBOM ID does not exist — check SBOM existence first using existing `SbomService::fetch` or a direct query.
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for the new model file.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` for the new service method.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `entity/src/sbom_advisory.rs::sbom_advisory` — existing SBOM-Advisory join table entity; use this for querying advisory-SBOM relationships instead of creating new queries
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing struct that includes the severity field; reference this for severity enumeration values
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse filtering utilities if applicable to the aggregation query
- `common/src/error.rs::AppError` — existing error enum implementing `IntoResponse`; use for error propagation

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] `SbomService::get_advisory_severity_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Method returns an appropriate error when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: `get_advisory_severity_summary` returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: `get_advisory_severity_summary` deduplicates advisories linked through multiple paths
- [ ] Unit test: `get_advisory_severity_summary` returns an error for a non-existent SBOM ID

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:880008b38987eaed572e7f51a838647145e6222934b6e281a44e2e1483a0d37a

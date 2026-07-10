## Repository
trustify-backend

## Target Branch
main

## Description
Add an `AdvisorySeveritySummary` model struct and a service method that aggregates vulnerability advisory severity counts for a given SBOM. The model represents the response shape `{ critical, high, medium, low, total }` with deduplication by advisory ID. The service method queries the existing `sbom_advisory` join table and groups counts by severity level.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with fields: critical, high, medium, low, total

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export the new struct
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries the sbom_advisory join table grouped by severity

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for struct definition and derive macros (Serialize, Deserialize, Debug, Clone, utoipa::ToSchema).
- The aggregation query should join `entity/src/sbom_advisory.rs` with `entity/src/advisory.rs` to access the severity field from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- Use SeaORM query builder for the aggregation — count distinct advisory IDs grouped by severity level.
- Return `AppError` on failure, consistent with existing service methods in `sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap errors with `.context()`.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust syntax scope.
- Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure for the new functionality.
  Applies: convention has no file-type restriction (broadly applicable).
- Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` if applicable for the aggregation query.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct; follow the same derive macros and serialization patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field needed for grouping; reference for understanding the severity data model
- `common/src/db/query.rs` — shared query builder helpers for filtering and aggregation

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] `SbomService::get_advisory_summary` method returns correct severity counts for a given SBOM ID
- [ ] Advisory counts are deduplicated by advisory ID
- [ ] Method returns `AppError` when the query fails

## Test Requirements
- [ ] Unit test for `get_advisory_summary` with a known set of advisories at various severity levels
- [ ] Test that duplicate advisories (same advisory linked multiple times) are counted only once
- [ ] Test that an SBOM with zero advisories returns all-zero counts

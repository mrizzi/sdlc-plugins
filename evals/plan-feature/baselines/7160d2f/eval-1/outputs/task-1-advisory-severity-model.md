## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for an SBOM. This struct will be returned by the new advisory-summary endpoint and contains fields for each severity level count (critical, high, medium, low) plus a total count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — AdvisorySeveritySummary struct with critical, high, medium, low, and total fields, deriving Serialize and ToSchema for OpenAPI generation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary` and re-export the AdvisorySeveritySummary struct

## Implementation Notes
- Follow the existing model struct pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) — derive `serde::Serialize`, `serde::Deserialize`, `utoipa::ToSchema`, and `Clone`/`Debug` as needed.
- All count fields should be typed as `i64` or `u64` consistent with how counts are represented in existing model structs.
- The struct should include:
  - `critical: i64` — count of critical severity advisories
  - `high: i64` — count of high severity advisories
  - `medium: i64` — count of medium severity advisories
  - `low: i64` — count of low severity advisories
  - `total: i64` — total unique advisory count
- Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for how severity is represented in the existing advisory model — the aggregation will group by this field.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct demonstrating the derive macros and module registration pattern to follow
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition that the aggregation will group by

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with critical, high, medium, low, and total fields
- [ ] Struct derives Serialize, Deserialize, ToSchema, Clone, and Debug
- [ ] Struct is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Unit test verifying AdvisorySeveritySummary can be serialized to JSON with the expected field names `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from JSON produces the correct struct values

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors

## Dependencies
- None (this is the first task)

## Repository
trustify-backend

## Description
Define the response model for the advisory severity summary endpoint. This struct represents the aggregated severity counts (`critical`, `high`, `medium`, `low`, `total`) returned by `GET /api/v2/sbom/{id}/advisory-summary`. The model is needed before the service or endpoint layers can be built.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New struct `AdvisorySeveritySummary` with fields for each severity level count and total

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` to expose the new model module

## Implementation Notes
- Follow the pattern established by existing model structs in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`).
- The struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema` (consistent with other response models in the crate).
- Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Reference the severity field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to ensure the severity enum values align with the count buckets.
- The struct lives in the `sbom` module (not `advisory`) because it is scoped to a specific SBOM's advisory breakdown.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field whose enum variants define the buckets this model aggregates over

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct compiles and is publicly exported from `modules/fundamental/src/sbom/model/`
- [ ] Struct has fields `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `ToSchema`
- [ ] Module re-export added to `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test that constructs an `AdvisorySeveritySummary` with known values and asserts all fields are correctly set
- [ ] Unit test that serializes `AdvisorySeveritySummary` to JSON and verifies the output matches `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

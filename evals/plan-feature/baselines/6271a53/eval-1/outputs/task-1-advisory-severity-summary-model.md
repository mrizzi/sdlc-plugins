# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new response model struct `AdvisorySeveritySummary` to represent the aggregated severity counts for advisories linked to an SBOM. This model will be used by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to return a structured severity breakdown. The struct must include fields for each severity level (critical, high, medium, low) and a total count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields, deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export the new struct

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct layout, derives, and serde configuration.
- All count fields should be typed as `i64` (or the equivalent integer type used by the existing models for count/quantity fields).
- Include `#[serde(rename_all = "camelCase")]` or snake_case serialization depending on the convention observed in sibling model structs (e.g., `SbomSummary`).
- Per constraints doc section 5.2: inspect the existing model files before implementing to confirm the exact derive macros and serde attributes used.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde configuration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for how the advisory severity field is represented (enum or string)

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] Struct derives `Serialize`, `Deserialize` and is publicly exported from the sbom model module
- [ ] Struct follows the same patterns (derives, serde attributes) as sibling model structs

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to JSON with expected field names
- [ ] Unit test verifying deserialization from JSON produces correct field values

## Dependencies
- None

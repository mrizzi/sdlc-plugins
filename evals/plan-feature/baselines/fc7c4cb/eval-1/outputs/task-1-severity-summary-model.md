## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct to represent aggregated advisory severity counts for an SBOM. This struct will hold the counts for each severity level (critical, high, medium, low) plus a total count, and will be used as the response body for the new advisory summary endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — new struct defining the AdvisorySeveritySummary response shape with fields: critical, high, medium, low, total

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export the new struct

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definition style, derive macros, and serialization attributes.
- The struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` at minimum, consistent with sibling model structs.
- Field types should be `i64` or `u64` for counts — inspect `modules/fundamental/src/sbom/model/summary.rs` to determine the exact integer type used by sibling models.
- The struct fields must match the API contract: `critical`, `high`, `medium`, `low`, `total` — all integer counts.
- Re-export the struct from `modules/fundamental/src/sbom/model/mod.rs` so it is accessible as `crate::sbom::model::AdvisorySeveritySummary`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for model struct conventions (derives, serde attributes, field types)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; inspect to determine the severity enum or type used

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] Struct derives serialization traits consistent with sibling models
- [ ] Struct is publicly re-exported from the sbom model module
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify `AdvisorySeveritySummary` serializes to JSON matching the expected shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify deserialization round-trip produces identical values

[sdlc-workflow] Description digest: sha256:9816d06a9fb4085970b395b38b13c43804c3a7538df04a809534473ea1c9b84d

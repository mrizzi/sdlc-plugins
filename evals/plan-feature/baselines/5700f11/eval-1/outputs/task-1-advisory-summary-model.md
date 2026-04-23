## Repository
trustify-backend

## Description
Define the `AdvisorySeveritySummary` response model struct that represents the severity aggregation result. This struct will be returned by the new advisory-summary endpoint and contains counts of advisories at each severity level plus a total. This is the foundational data type that the service layer and endpoint will depend on.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod severity_summary;` to expose the new model submodule

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` — Define the `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Implementation Notes
- Follow the pattern used by `modules/fundamental/src/sbom/model/summary.rs` for the `SbomSummary` struct: derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and implement `utoipa::ToSchema` for OpenAPI generation.
- The struct lives under the `sbom` module (not `advisory`) because it is conceptually a summary view of an SBOM's advisory landscape, consistent with how `SbomSummary` and `SbomDetails` are organized in `modules/fundamental/src/sbom/model/`.
- Reference `modules/fundamental/src/advisory/model/summary.rs` for how the `severity` field is represented on individual advisories — the aggregation will group by that same severity enum.
- Use `u64` for count fields to match Rust conventions for non-negative counts.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the same derive macros, serde attributes, and module registration pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference the `severity` field type to ensure consistency in severity representation

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Struct implements `utoipa::ToSchema` for OpenAPI docs
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with the new model

## Test Requirements
- [ ] Unit test that `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test that `AdvisorySeveritySummary` deserializes from valid JSON

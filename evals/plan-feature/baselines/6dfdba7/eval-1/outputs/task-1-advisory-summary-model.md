## Repository
trustify-backend

## Description
Define the `AdvisorySeveritySummary` response model that represents aggregated severity counts for advisories linked to an SBOM. This struct is the data contract returned by the new `/api/v2/sbom/{id}/advisory-summary` endpoint. It must include fields for `critical`, `high`, `medium`, `low`, and `total` counts, matching the API specification in TC-9001. The struct also needs an optional `threshold` concept for filtering, though filtering logic itself belongs in the service layer.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New file containing the `AdvisorySeveritySummary` struct with serde Serialize/Deserialize derives and utoipa ToSchema for OpenAPI generation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the pattern established by `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for derive macros, serde attributes, and module organization.
- The struct should derive `Clone, Debug, Serialize, Deserialize, PartialEq, Eq` plus `utoipa::ToSchema` if the project uses utoipa for OpenAPI docs.
- Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. All unsigned integers representing counts.
- Check the existing `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for how severity is represented (likely an enum or string field). The aggregation model should align with those severity level names.
- Keep the struct in the sbom model namespace since it represents an SBOM-scoped aggregation, not a standalone advisory concept.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct layout, derive macros, and serde conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition; use the same severity level names

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] Struct derives Serialize, Deserialize, and any schema traits used by existing models
- [ ] Struct is publicly re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check -p trustify-fundamental`)

## Verification Commands
- `cargo check -p trustify-fundamental` — should compile without errors

## Repository
trustify-backend

## Description
Define the `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for a given SBOM. This struct will be returned by the new advisory-summary endpoint and must include fields for each severity level plus a total count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New model struct `AdvisorySeveritySummary` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration to expose the new model module

## Implementation Notes
Follow the pattern established by existing model structs in the SBOM module. Reference `modules/fundamental/src/sbom/model/summary.rs` for the `SbomSummary` struct pattern -- it derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and uses `utoipa::ToSchema` for OpenAPI schema generation. The new struct should derive the same traits. The severity levels should match the values used in `modules/fundamental/src/advisory/model/summary.rs` where the `AdvisorySummary` struct includes a `severity` field. Ensure the struct is compatible with Axum's `Json<T>` response extraction by implementing `Serialize`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow its derive macros and struct conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field values and naming

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`
- [ ] Module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors

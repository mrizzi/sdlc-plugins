## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the severity aggregation response shape: `{ critical, high, medium, low, total }`. This struct will be used by the service layer and endpoint handler in subsequent tasks.

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` -- Defines the `AdvisorySeveritySummary` struct with fields `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod severity_summary;` to register the new submodule and re-export `AdvisorySeveritySummary`.

## Implementation Notes
Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. These sibling files define structs with serde derives and utoipa schema annotations. The new struct should use the same derive set and module registration pattern visible in `modules/fundamental/src/sbom/model/mod.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Follow the same struct definition pattern (derives, visibility, field types)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Reference this to confirm the severity field type used in the advisory domain

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/severity_summary.rs`
- [ ] Struct has fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema`
- [ ] Module is registered in `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles with `cargo check`

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Verify the struct can be deserialized from a JSON object with those fields

## Verification Commands
- `cargo check -p trustify-fundamental` -- compiles without errors

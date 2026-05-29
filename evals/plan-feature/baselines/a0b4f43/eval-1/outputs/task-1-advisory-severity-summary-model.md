## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for a given SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct contains fields for each severity level (critical, high, medium, low) and a total count, all as unsigned integers. It must derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI documentation generation.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New file defining the `AdvisorySeveritySummary` struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). These files demonstrate the struct definition style, derive macros, and module re-export conventions used throughout the codebase.
- The struct fields should be: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Derive `serde::Serialize`, `serde::Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` to match the patterns in sibling model structs.
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to the listed files only. Follow patterns referenced in Implementation Notes (constraint 5.3).

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Demonstrates the model struct pattern with serde derives and utoipa schema derivation used in this module
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition that this summary will aggregate across

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct contains fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Verify the struct can be deserialized from a JSON object with integer severity counts

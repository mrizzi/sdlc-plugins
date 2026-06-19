## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the severity count breakdown for advisories linked to an SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. It contains fields for each severity level (`critical`, `high`, `medium`, `low`) and a `total` count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New module defining the `AdvisorySeveritySummary` struct

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export the struct

## Implementation Notes
Follow the pattern established by existing model structs in the same directory. The `SbomSummary` struct in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` demonstrate the expected pattern: derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and use `utoipa::ToSchema` for OpenAPI spec generation.

The new struct should have these fields:
- `critical: i64`
- `high: i64`
- `medium: i64`
- `low: i64`
- `total: i64`

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure by placing the model in the `model/` subdirectory.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Framework: use Axum/SeaORM derives and patterns consistent with the existing model structs.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct derive macros, serde attributes, and utoipa schema annotations
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for the model definition pattern used in the sbom module

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names
- [ ] Verify the struct can be deserialized from JSON
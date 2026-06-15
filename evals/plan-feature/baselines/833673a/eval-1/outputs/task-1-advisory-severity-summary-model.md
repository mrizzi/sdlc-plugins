## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct to the SBOM model layer. This struct represents the JSON response shape for the new advisory severity aggregation endpoint: `{ critical: i64, high: i64, medium: i64, low: i64, total: i64 }`. It will be used by the service layer (Task 2) and endpoint handler (Task 3) to return aggregated severity counts for a given SBOM.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — new module defining the `AdvisorySeveritySummary` struct with Serialize derive

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export the struct

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct layout, derive macros, and module re-exports.
- The struct should derive `serde::Serialize`, `Debug`, and `Clone` at minimum, consistent with other model structs in the same directory.
- Fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`. Use `i64` to match SeaORM's default integer mapping for COUNT aggregations.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` matching the convention's model directory scope.
- Per Key Conventions §Response types: this struct is a direct response type (not paginated), so it does not wrap in `PaginatedResults<T>`. Applies: task creates `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` matching the convention's Rust model file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde configuration in the sbom model layer
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reference for how severity is represented in the existing domain model

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_severity_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize`, `Debug`, `Clone`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Verify the struct can be instantiated and serialized to JSON with the expected field names
- [ ] Verify the JSON output matches the expected shape: `{"critical":0,"high":0,"medium":0,"low":0,"total":0}`

[sdlc-workflow] Description digest: sha256-md:c097576f47e0dcad418d20a7a2f44670b28215992d89e0e5e28c372356567d04

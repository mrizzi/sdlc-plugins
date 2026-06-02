## Repository
trustify-backend

## Target Branch
main

## Description
Add a `SeveritySummary` response model struct to the SBOM model module. This struct represents the aggregated advisory severity counts for a given SBOM and will be returned by the new advisory-summary endpoint. The struct must include fields for `critical`, `high`, `medium`, `low`, and `total` counts, all as integers. It must derive `Serialize` so it can be returned as JSON from an Axum handler.

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` — New `SeveritySummary` struct with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Re-export the new `SeveritySummary` struct

## Implementation Notes
Follow the existing model pattern established in the SBOM model module. The `SbomSummary` struct in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` demonstrate the expected model conventions: derive `Serialize`, use `serde` attributes as needed, and re-export from `model/mod.rs`.

The struct fields should be:
- `critical: i64`
- `high: i64`
- `medium: i64`
- `low: i64`
- `total: i64`

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure by placing the new model in the `model/` subdirectory and re-exporting from `mod.rs`.
Applies: task creates `modules/fundamental/src/sbom/model/severity_summary.rs` matching the convention's Rust module file scope.

Per CONVENTIONS.md §Error handling: derive appropriate traits consistent with other model structs.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Existing SBOM model struct; follow its derive macros, serde configuration, and module re-export pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field definition that maps to the severity levels this struct aggregates

## Acceptance Criteria
- [ ] `SeveritySummary` struct exists in `modules/fundamental/src/sbom/model/severity_summary.rs` with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Struct derives `Serialize` for JSON serialization
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Verify the struct can be instantiated and serialized to JSON with expected field names
- [ ] Verify all fields are present in the serialized output

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors

# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct will be used as the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for each severity level (critical, high, medium, low) and a total count, following the existing model patterns in the SBOM module.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new model struct `AdvisorySeveritySummary` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`, deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct derivation macros and module organization.
- The struct should derive `serde::Serialize` and `serde::Deserialize` so it can be returned as a JSON response via Axum.
- Use `u64` for count fields to match Rust's unsigned integer conventions for counts.
- Register the module in the parent `mod.rs` and re-export the type, following the same pattern used for `SbomSummary` and `SbomDetails`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for model struct pattern, derive macros, and module registration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for how advisory-related model structs are defined; includes the severity field that this task's model aggregates

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all unsigned integers)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`
- [ ] Module is registered and type is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with the new model

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Verify the struct can be deserialized from JSON
- [ ] Verify default/zero-value construction produces `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`

## Verification Commands
- `cargo build -p trustify-fundamental` — expected outcome: compiles without errors
- `cargo test -p trustify-fundamental` — expected outcome: model tests pass

## Dependencies
- None

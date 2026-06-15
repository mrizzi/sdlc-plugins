# Task 1: Create advisory severity summary response model

## Repository

trustify-backend

## Target Branch

main

## Description

Define the `AdvisorySeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM. This model provides the response shape for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint: `{ critical, high, medium, low, total }`. The struct must derive Serialize so it can be returned as JSON from Axum handlers, following the same patterns used by existing model structs like `SbomSummary` and `AdvisorySummary`.

## Files to Create

- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` -- new struct file for the `AdvisorySeveritySummary` response type

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod advisory_severity_summary;` and re-export the struct

## Implementation Notes

- Follow the model pattern in `modules/fundamental/src/sbom/model/summary.rs` for struct layout and derive macros. Existing model structs derive `Serialize`, `Debug`, and `Clone`.
- The struct fields should be: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Register the module in `modules/fundamental/src/sbom/model/mod.rs` using the same `pub mod` + `pub use` pattern as `summary` and `details` modules.
- The `severity` field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` provides the enum or string type used for severity classification -- reference it to ensure consistency in severity level naming.

### Applicable Conventions

- **Module pattern**: Applies: task creates `advisory_severity_summary.rs` matching the convention's model directory scope (`modules/fundamental/src/sbom/model/`).

## Acceptance Criteria

- [ ] `AdvisorySeveritySummary` struct exists with fields `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Debug`, `Clone`
- [ ] Struct is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Compiles without warnings

## Test Requirements

- [ ] Unit test verifies `AdvisorySeveritySummary` serializes to expected JSON shape `{"critical":0,"high":0,"medium":0,"low":0,"total":0}`
- [ ] Unit test verifies `total` field is independent (not auto-computed) -- the service layer is responsible for computing it

[Description digest: sha256-md:a3f7b2c91d4e8f0a56b3c2d1e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0 would be posted as a comment]

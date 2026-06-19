## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents the severity count aggregation for advisories linked to an SBOM. This struct will be returned by the new advisory-summary endpoint. It must include fields for critical, high, medium, low, and total counts, serialized as JSON with lowercase field names.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with serde Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` to expose the new model

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails): derive `Clone, Debug, Serialize, Deserialize` and use `serde(rename_all = "camelCase")` if that is the existing convention, or snake_case matching the feature spec's `{ critical: N, high: N, medium: N, low: N, total: N }` shape.
- The struct fields should be: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`.
- Per Module pattern convention: each domain module follows model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's model directory scope.
- Per Error handling convention: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the same derive macros, serde attributes, and struct layout pattern for consistency
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference the severity field type used in the advisory model to ensure type compatibility

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: critical, high, medium, low, total (all integer types)
- [ ] Struct derives Serialize and Deserialize
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] `cargo check` passes with the new model struct
- [ ] Verify the struct can be serialized to JSON matching the expected shape `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`

## Verification Commands
- `cargo check -p trustify-fundamental` — expected: compilation succeeds with no errors

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `AdvisorySeveritySummary` response model struct to represent aggregated advisory severity counts for a given SBOM. This struct will be used as the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for `critical`, `high`, `medium`, `low`, and `total` counts, all as unsigned integers, and derive `Serialize` for JSON serialization.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — new model struct `AdvisorySeveritySummary` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`): derive `Clone`, `Debug`, `Serialize`, `Deserialize`, `utoipa::ToSchema` (if utoipa is used in sibling models).
- The struct does not map to a database entity directly — it is a computed response type, not a SeaORM entity. Do not add it to `entity/src/`.
- Reference `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) for how the severity field is represented in existing advisory models — ensure the severity levels used in this struct align with the enum or string values used there.
- Per the feature requirements, `total` is the sum of all four severity counts.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the model struct pattern (derive macros, field types) to follow for the new struct
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition that the aggregation will count against

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_severity_summary.rs`
- [ ] Struct has fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize` and is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify the struct can be instantiated and serialized to JSON with the expected field names
- [ ] Verify the `total` field is independent (not auto-computed) — it is the caller's responsibility to set it correctly

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors

## Dependencies
- None

[sdlc-workflow] Description digest: sha256:87a21401fd4e7cf35a29283da27f9be047dd81dd8a6c37fa51be6c0c4e32245b

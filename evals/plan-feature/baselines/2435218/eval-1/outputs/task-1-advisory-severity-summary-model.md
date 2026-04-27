# Task 1 — Add AdvisorySeveritySummary Response Model

## Repository
trustify-backend

## Description
Add a new `AdvisorySeveritySummary` response model struct to the SBOM module that represents the severity count breakdown for advisories linked to an SBOM. This struct will be the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model must include fields for each severity level (critical, high, medium, low) and a total count, with Serialize/Deserialize derives for JSON serialization.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new struct `AdvisorySeveritySummary` with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the pattern established by existing model structs in the same module. Reference `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for derive macros, visibility, and naming conventions.
- The struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `PartialEq` at minimum, consistent with sibling model structs.
- Reference `modules/fundamental/src/advisory/model/summary.rs` for how severity is represented in the existing advisory model — the aggregation will group by this severity field.
- Do not introduce a new severity enum; reuse whatever severity type the advisory entity already uses (see `entity/src/advisory.rs`).
- Per constraints doc section 5: inspect existing model files before writing to ensure pattern consistency.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and module registration pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains severity field; reference for severity type

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all integer counts)
- [ ] Struct derives `Serialize` and `Deserialize` for JSON response serialization
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify struct can be serialized to JSON with expected field names (unit test)
- [ ] Verify struct can be deserialized from JSON (round-trip test)

## Verification Commands
- `cargo check -p trustify-fundamental` — project compiles without errors

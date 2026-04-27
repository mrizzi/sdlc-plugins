# Task 1 — Add AdvisorySeveritySummary model

## Repository
trustify-backend

## Description
Add a new `AdvisorySeveritySummary` model struct to represent aggregated advisory severity counts for an SBOM. This model is the response shape for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. It holds deduplicated counts of advisories at each severity level (critical, high, medium, low) plus a total count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New model struct `AdvisorySeveritySummary` with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`). Each model struct derives `Clone, Debug, Serialize, Deserialize` and uses `serde` for JSON serialization.
- The struct should derive `utoipa::ToSchema` if the project uses utoipa for OpenAPI spec generation (check existing model structs for this pattern).
- The `total` field is the sum of all severity counts, provided for convenience so consumers do not need to compute it client-side.
- Per `docs/constraints.md` §5.4: Do not duplicate existing model patterns — reuse the same derive macros and serde conventions used by sibling model structs.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for model struct conventions (derives, serde attributes, module re-export pattern)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field definition showing how severity is represented in the existing codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all integer types)
- [ ] Struct derives serialization traits consistent with existing models
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to JSON with the expected field names: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from JSON round-trips correctly

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors

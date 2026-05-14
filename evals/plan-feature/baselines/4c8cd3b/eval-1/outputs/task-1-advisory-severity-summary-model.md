## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents the severity
breakdown returned by the new advisory-summary endpoint. This struct holds deduplicated
counts of advisories at each severity level (critical, high, medium, low) plus a total
count. It serves as the response type for `GET /api/v2/sbom/{id}/advisory-summary`.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new struct `AdvisorySeveritySummary` with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern used by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` — derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and any other derives used on sibling model structs.
- The struct should derive `serde::Serialize` so it can be returned as a JSON response from an Axum handler.
- Place the file alongside `summary.rs` and `details.rs` in `modules/fundamental/src/sbom/model/` to follow the established module-per-model convention.
- Use `i64` for count fields to match PostgreSQL `COUNT(*)` return types and avoid unnecessary casting in the service layer.
- The `total` field is the sum of all severity counts and is included for consumer convenience.
- Per `docs/constraints.md` section 5 (Code Change Rules): changes must be scoped to the files listed, and implementation must follow existing patterns in the codebase.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde annotations used in SBOM model types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for how advisory-related models are structured, especially the severity field definition

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone` (minimum)
- [ ] `modules/fundamental/src/sbom/model/mod.rs` re-exports `AdvisorySeveritySummary`
- [ ] Project compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify `AdvisorySeveritySummary` serializes to the expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify deserialization round-trip produces identical struct values

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

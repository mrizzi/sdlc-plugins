# Task 1 — Add AdvisorySeveritySummary Response Model

## Repository
trustify-backend

## Description
Add a new `AdvisorySeveritySummary` struct to the SBOM model module that represents the response shape for the advisory severity aggregation endpoint. This struct provides a compact summary of how many advisories at each severity level affect a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new summary struct

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define the `AdvisorySeveritySummary` struct

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: response body shape `{ critical: u64, high: u64, medium: u64, low: u64, total: u64 }`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`).
- The struct should derive `Serialize`, `Deserialize`, `Clone`, `Debug` to match existing model conventions.
- Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- The `total` field is the sum of all severity counts and represents the total number of unique advisories affecting the SBOM.
- Do NOT use `PaginatedResults<T>` from `common/src/model/paginated.rs` — this is a single aggregated response, not a list.
- Reference `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) which includes the `severity` field to understand how severity is represented in the existing codebase.
- Per `docs/constraints.md` §4.6: file paths must be real paths discovered during repository analysis.
- Per `docs/constraints.md` §5.3: follow patterns referenced in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct; follow its derive macros, visibility, and module registration pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition; reference its type to ensure the aggregation model aligns with how severity is represented

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct compiles without errors

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names: `{"critical":0,"high":0,"medium":0,"low":0,"total":0}`
- [ ] Verify the struct can be deserialized from a JSON payload

## Verification Commands
- `cargo check -p trustify-module-fundamental` — should compile without errors

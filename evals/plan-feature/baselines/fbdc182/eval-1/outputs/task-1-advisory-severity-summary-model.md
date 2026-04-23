## Repository
trustify-backend

## Description
Define the `AdvisorySeveritySummary` response struct that the new aggregation endpoint will serialize and return. This struct holds per-severity counts and a total, and is the wire type for `GET /api/v2/sbom/{id}/advisory-summary`. Creating the model in its own file keeps the sbom module's model layer consistent with the existing pattern used by `SbomSummary` and `SbomDetails`.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields (all `u32`), deriving `serde::Serialize`, `Debug`, and `Default`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
Follow the pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`:

- Derive `serde::Serialize` (and `serde::Deserialize` if the struct may appear in query helpers) using `#[derive(Debug, Default, serde::Serialize, serde::Deserialize)]`.
- Field names must match the JSON shape specified in the feature: `critical`, `high`, `medium`, `low`, `total`. Use `#[serde(rename_all = "camelCase")]` only if the rest of the API uses camelCase — check `modules/fundamental/src/sbom/model/summary.rs` for the project convention before choosing.
- `total` is the sum of the four severity counts; populate it in the service layer rather than relying on the DB to compute it, for clarity.
- Add a `pub fn add_advisory(&mut self, severity: &str)` helper method on the struct so the service method can accumulate counts without repeating match logic. Match on lowercase severity strings (`"critical"`, `"high"`, `"medium"`, `"low"`) and increment `total` in every branch.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` already has a `severity` field — inspect that file to confirm the exact type (likely `String` or an enum) before writing the match arms.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout and derive macros
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — provides the `severity` field type used in the service layer

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` is publicly re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct serializes to `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }` for the default value
- [ ] `add_advisory("critical")` increments `critical` and `total` by 1; unknown severity strings increment only `total`
- [ ] `cargo check -p fundamental` passes with no warnings

## Test Requirements
- [ ] Unit test in `advisory_severity_summary.rs`: call `add_advisory` for each severity level and assert all fields equal expected counts
- [ ] Unit test: call `add_advisory("unknown")` and assert only `total` increments

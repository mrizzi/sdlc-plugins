## Repository
trustify-backend

## Description
Add an `AdvisorySeveritySummary` response model struct that represents aggregated advisory severity counts for a given SBOM. This struct will be used as the response body for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must include fields for each severity level (critical, high, medium, low) and a total count.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New model struct `AdvisorySeveritySummary` with severity count fields

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails` struct) — these derive `Serialize`, `Deserialize`, and implement `IntoResponse` via the framework conventions.
- The `AdvisorySeveritySummary` struct should have the following fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Reference the severity field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to understand how severity values are represented in the existing codebase — the aggregation query (Task 2) will group by this field.
- Per the repository's key conventions: the framework is Axum for HTTP and SeaORM for database. All response types follow the pattern in the `model/` subdirectory of each domain module.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow its derive macros, field documentation style, and module export pattern as the template for the new struct.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field definition; understand the severity enum/type to ensure compatibility with aggregation queries.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize` and `Deserialize`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Verify that `AdvisorySeveritySummary` can be serialized to JSON with the expected field names: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify that `AdvisorySeveritySummary` can be deserialized from a valid JSON payload

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

# Task 1 — Add AdvisorySeveritySummary model struct

## Repository
trustify-backend

## Description
Create a new `AdvisorySeveritySummary` struct to represent the aggregated severity counts response for the advisory-summary endpoint. This struct serves as the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint and must serialize to `{ critical, high, medium, low, total }`.

## Files to Modify
- `modules/fundamental/src/advisory/model/mod.rs` — add `pub mod severity_summary;` to module declarations

## Files to Create
- `modules/fundamental/src/advisory/model/severity_summary.rs` — define `AdvisorySeveritySummary` struct with serde Serialize/Deserialize and utoipa ToSchema derives

## Implementation Notes
- Follow the existing model pattern used by `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — each model struct derives `Clone, Debug, Serialize, Deserialize` and `utoipa::ToSchema`.
- The struct fields should be: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Reference `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for how model structs are organized in this codebase.
- Per constraints §4.6/§4.7: file paths are based on the established `model/` directory structure in the advisory module.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for struct derive macros and serialization patterns
- `common/src/model/paginated.rs::PaginatedResults` — reference for how response wrapper types are structured

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`
- [ ] Struct is publicly exported from `modules/fundamental/src/advisory/model/mod.rs`

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from valid JSON produces correct struct values

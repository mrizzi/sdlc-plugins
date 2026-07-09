## Repository
trustify-backend

## Target Branch
main

## Description
Add a `SeveritySummary` response model struct to represent the aggregated advisory severity counts for a given SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct includes fields for `critical`, `high`, `medium`, `low`, and `total` counts, matching the response shape defined in feature TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` — defines the `SeveritySummary` struct with serde serialization

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod severity_summary;` and re-export `SeveritySummary`

## Implementation Notes
- Define `SeveritySummary` as a public struct with `#[derive(Clone, Debug, Serialize, Deserialize, utoipa::ToSchema)]` to enable JSON serialization and OpenAPI schema generation.
- Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- Follow the existing model patterns in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for derive macros and struct organization.
- Per CONVENTIONS.md §Module Pattern: place the new model file in the `model/` subdirectory of the `sbom` domain module, following the established `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/model/summary.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/severity_summary.rs` matching the convention's model/ directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct organization, derive macros, and serde attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for the `severity` field type used in advisory records

## Acceptance Criteria
- [ ] `SeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, and `total` fields of type `u64`
- [ ] Struct derives `Serialize`, `Deserialize`, and OpenAPI schema traits
- [ ] Struct is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Verify `SeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify deserialization round-trip produces identical values

## Dependencies
- None

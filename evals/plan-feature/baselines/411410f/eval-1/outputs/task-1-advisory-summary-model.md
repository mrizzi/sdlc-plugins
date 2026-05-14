## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM. This struct is the foundation for the service query and endpoint handler in subsequent tasks. It must serialize to JSON matching the contract: `{ critical, high, medium, low, total }`.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define `AdvisorySeveritySummary` struct with `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64` fields. Derive `Serialize`, `Deserialize`, `Clone`, `Debug`, `Default`, and `utoipa::ToSchema` for OpenAPI generation.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration and re-export `AdvisorySeveritySummary` so it is accessible from `sbom::model::AdvisorySeveritySummary`.

## Implementation Notes
- Follow the pattern established by `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct definition style: derive macros, field visibility, and documentation comments.
- The struct should derive `utoipa::ToSchema` to integrate with the existing OpenAPI spec generation, consistent with how `SbomSummary` and `AdvisorySummary` are defined.
- Include `#[serde(rename_all = "camelCase")]` if existing model structs use camelCase serialization — check `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/advisory/model/summary.rs` for the prevailing convention and match it.
- The `total` field should be computed as the sum of all severity levels, but stored as a materialized field rather than computed at serialization time, to match the flat JSON response contract.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct compiles and is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct has fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `Default`
- [ ] Struct derives `utoipa::ToSchema` for OpenAPI spec integration
- [ ] Serialization matches the expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

## Test Requirements
- [ ] Unit test that constructs an `AdvisorySeveritySummary` with known values and asserts `serde_json::to_value` produces the expected JSON structure
- [ ] Unit test that deserializes a valid JSON string into `AdvisorySeveritySummary` and verifies field values

## Dependencies
- None — this is the first task in the dependency chain

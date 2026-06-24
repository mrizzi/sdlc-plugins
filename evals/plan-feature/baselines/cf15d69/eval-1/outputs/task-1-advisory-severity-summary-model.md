## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, containing counts for critical, high, medium, and low severities plus a total. A corresponding `SeverityThreshold` enum is also needed for the optional `?threshold` query parameter filtering.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`; derives `Serialize`, `Deserialize`, `ToSchema` (for OpenAPI); also contains `SeverityThreshold` enum for query param deserialization

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary` and `SeverityThreshold`

## Implementation Notes
Follow the existing model pattern from `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. The struct should derive `serde::Serialize`, `serde::Deserialize`, and `utoipa::ToSchema` consistent with `SbomSummary` and `SbomDetails`. The `SeverityThreshold` enum should have variants `Critical`, `High`, `Medium`, `Low` and derive `Deserialize` for query param parsing.

Per Key Conventions (Module pattern): Follow `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module pattern scope.

Per Key Conventions (Framework): Use SeaORM-compatible derive macros and Axum-compatible serialization. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` files scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, and `ToSchema`
- [ ] `SeverityThreshold` enum is defined with variants for each severity level
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles with `cargo check -p trustify-fundamental`

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying `SeverityThreshold` deserializes from query string values

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental model::advisory_summary` — model unit tests pass

[sdlc-workflow] Description digest: sha256-md:ba71d3eefbd7593007a6ffb76249b182c5a442a4eee0a0a7069985e2371ceaa3

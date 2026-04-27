## Repository
trustify-backend

## Description
Add a new `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This model is the response shape for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. It contains counts for each severity level (critical, high, medium, low) plus a total count, enabling frontend dashboard widgets and alerting integrations to retrieve a pre-computed severity breakdown in a single API call.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — new struct `AdvisorySeveritySummary` with fields `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`, deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`, and implementing `IntoResponse`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_severity_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`. Each model struct in the codebase derives serde traits and lives in its own file within the `model/` subdirectory.
- The struct should use `u64` for count fields to handle large advisory sets without overflow.
- Derive `utoipa::ToSchema` if the project uses utoipa for OpenAPI generation (check existing model structs for this derive).
- Per `docs/constraints.md` section 5 (Code Change Rules): changes must be scoped to the files listed; inspect existing model files before writing to match their patterns exactly.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and module re-export pattern
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — reference for how detail-level response models are structured
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition showing how severity is represented in the existing codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles successfully (`cargo check`)

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from valid JSON produces correct field values

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors

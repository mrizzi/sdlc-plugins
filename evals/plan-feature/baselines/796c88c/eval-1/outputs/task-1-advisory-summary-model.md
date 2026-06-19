## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response model that represents aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model needs to serialize to JSON with fields: `critical`, `high`, `medium`, `low`, and `total`.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New struct `AdvisorySeveritySummary` with `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`, deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, `utoipa::ToSchema`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` for struct layout and derive macros.
- The struct does not wrap `PaginatedResults<T>` since this is a single aggregate object, not a list.
- Include `#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, Eq)]` and `#[derive(utoipa::ToSchema)]` to match existing model conventions.
- All count fields should be `u64` to match Rust's unsigned integer conventions for counts.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct layout, derive macros, and serde annotations
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Has the `severity` field definition showing the severity enum/string representation used in the codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `utoipa::ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Crate compiles without errors

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Applicable Conventions
- **Module pattern**: Applies: task modifies `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `model/` scope.

[sdlc-workflow] Description digest: sha256-md:3e2768063393756458d97b6f75a2a3c317a01eebab192923d1322d3e4610d3eb

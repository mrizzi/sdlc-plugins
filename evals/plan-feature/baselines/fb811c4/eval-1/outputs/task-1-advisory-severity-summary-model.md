## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This model is the foundation for the new endpoint and will be used by both the service layer and the endpoint handler.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Re-export the new `AdvisorySeveritySummary` struct from the model module

## Files to Create
- `modules/fundamental/src/sbom/model/severity_summary.rs` — Define the `AdvisorySeveritySummary` struct with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`

## Implementation Notes
Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails). The new struct should:

1. Derive `Clone`, `Debug`, `Serialize`, `Deserialize`, and `utoipa::ToSchema` to match the conventions used by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`.
2. Place the struct in a new file `modules/fundamental/src/sbom/model/severity_summary.rs` following the one-struct-per-file pattern seen with `summary.rs` and `details.rs`.
3. Add `pub mod severity_summary;` and a re-export in `modules/fundamental/src/sbom/model/mod.rs`.
4. All count fields should be `i64` to match PostgreSQL `COUNT(*)` return types used in SeaORM queries throughout the codebase.

Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure for the sbom domain module.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's module organization scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Crate compiles without errors (`cargo check -p trustify-fundamental`)

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

[sdlc-workflow] Description digest: sha256-md:73e8945ce58180ee050b4c82fcc28faf585a0501fb2072330867e9ed6707d84b

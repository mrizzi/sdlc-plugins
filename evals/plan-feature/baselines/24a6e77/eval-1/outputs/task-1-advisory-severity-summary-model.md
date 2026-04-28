# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Description
Create the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This model will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The struct must serialize to JSON with fields `critical`, `high`, `medium`, `low`, and `total`, all as integer counts. This is the foundational data structure that the service layer and endpoint handler will depend on.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — new struct `AdvisorySeveritySummary` with `critical`, `high`, `medium`, `low`, `total` fields, deriving `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, and implementing `utoipa::ToSchema` for OpenAPI generation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` for struct layout, derive macros, and module registration
- The struct fields should all be `i64` (or `u64`) to match database count return types — check the type used by `PaginatedResults<T>` in `common/src/model/paginated.rs` for count fields to maintain consistency
- Use `serde` derives for serialization and `utoipa::ToSchema` for OpenAPI schema generation, following the pattern of sibling model structs
- Per constraints (Section 4.6): file paths must be real paths discovered during analysis — the model directory pattern at `modules/fundamental/src/sbom/model/` is confirmed
- Per constraints (Section 4.7): reference existing patterns — the `SbomSummary` struct is the closest analog for struct layout

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the standard struct pattern with derive macros and module registration in this module
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — shows how complex model structs are structured with serialization support
- `common/src/model/paginated.rs::PaginatedResults` — reference for how count/total fields are typed in the codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct implements `utoipa::ToSchema` for OpenAPI documentation
- [ ] Project compiles successfully with the new model

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying deserialization from JSON into the struct

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-fundamental` — all tests should pass

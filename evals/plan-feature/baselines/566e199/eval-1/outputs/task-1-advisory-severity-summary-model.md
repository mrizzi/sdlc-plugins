# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new response model struct `AdvisorySeveritySummary` that represents the aggregated severity counts for advisories linked to an SBOM. This model will be returned by the new advisory-summary endpoint. It contains fields for each severity level (critical, high, medium, low) and a total count. The struct must derive Serialize for JSON response rendering.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to export the new model

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct layout, derive macros, and module registration.
- The struct must derive `serde::Serialize` and `utoipa::ToSchema` (or equivalent) for JSON serialization and OpenAPI documentation, consistent with sibling model structs.
- Do not add query logic in this task — the model is a pure data struct.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derive macros and serialization patterns used in SBOM models
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for the `severity` field type, which determines valid severity values for grouping

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `Serialize` for JSON response rendering
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`

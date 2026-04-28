# Task 1 — Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Description
Add a new response model struct `AdvisorySeveritySummary` to represent the aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model must include fields for each severity level (critical, high, medium, low) and a total count.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to the module declarations

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define the `AdvisorySeveritySummary` struct

## Implementation Notes
- Follow the pattern established by existing model structs such as `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs` for derive macros and struct organization.
- The struct fields should be:
  - `critical: i64`
  - `high: i64`
  - `medium: i64`
  - `low: i64`
  - `total: i64`
- Use `serde::Serialize` and `serde::Deserialize` derives, consistent with `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- Also define a `SeverityThreshold` enum or a `ThresholdQueryParam` struct with an optional `threshold` field of type `Option<String>` for the severity threshold filter, using `serde::Deserialize` and Axum's `Query` extractor pattern. Check whether query param structs live alongside endpoints or models in sibling code (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`); if they live in endpoints, defer the query param struct to Task 3.
- Per constraints doc section 5: code must not duplicate existing functionality. Check `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for the severity field type to ensure consistency.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and Serialize/Deserialize patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition; understanding its type informs how to aggregate severity levels
- `common/src/model/paginated.rs::PaginatedResults` — reference for how response wrapper types are structured in this codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with `critical`, `high`, `medium`, `low`, `total` integer fields
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, `PartialEq`
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test that `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test that `AdvisorySeveritySummary` deserializes from a valid JSON object

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — model tests should pass

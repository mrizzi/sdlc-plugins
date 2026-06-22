# Task 1 — Add advisory severity summary model

## Repository
trustify-backend

## Target Branch
main

## Description
Add an `AdvisorySeveritySummary` response model struct to represent aggregated advisory severity counts for an SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model captures counts for each severity level (critical, high, medium, low) plus a total, matching the response shape specified in the feature requirements.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with fields: critical (u64), high (u64), medium (u64), low (u64), total (u64)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) — derive Serialize, Deserialize, Clone, Debug, and any other traits used by sibling models.
- The struct should derive `serde::Serialize` and `serde::Deserialize` for JSON serialization via Axum responses.
- Use `u64` for count fields to match the general numeric patterns in the codebase. If sibling model structs use a different integer type (e.g., `i64`), match that type instead.
- This is a response-only DTO — no SeaORM entity or database table is needed. The struct aggregates data from existing `sbom_advisory` and `advisory` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde configuration
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field that will be used for aggregation grouping
- `common/src/model/paginated.rs::PaginatedResults` — reference for how response wrapper types are structured in this codebase

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total
- [ ] Struct derives Serialize and Deserialize (and other standard derives matching sibling models)
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Verify deserialization from JSON produces the correct field values

## Dependencies
- None

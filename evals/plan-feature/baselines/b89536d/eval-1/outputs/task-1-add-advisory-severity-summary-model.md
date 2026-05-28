# Task 1 -- Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new response model `AdvisorySeveritySummary` to represent aggregated advisory severity counts for an SBOM. This struct will be returned by the new advisory-summary endpoint and contains fields for critical, high, medium, low, and total counts. The model must support serialization via serde for JSON responses.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` -- new struct `AdvisorySeveritySummary` with fields: critical (u64), high (u64), medium (u64), low (u64), total (u64)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod advisory_summary;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern used by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`
- Derive `serde::Serialize`, `serde::Deserialize`, `Clone`, `Debug`, and any other derives used by sibling model structs
- The struct should use `u64` for count fields to match the database count return type
- Reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` to understand the existing severity field representation -- the aggregation model must align with the same severity classification (Critical, High, Medium, Low)
- Error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping (per `common/src/error.rs`)

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing SBOM model to follow for struct layout, derives, and serialization patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field definition to align severity classification with

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total
- [ ] Struct derives serde Serialize/Deserialize for JSON serialization
- [ ] Module is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct compiles without errors

## Test Requirements
- [ ] Unit test that verifies `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test that verifies deserialization from JSON round-trips correctly

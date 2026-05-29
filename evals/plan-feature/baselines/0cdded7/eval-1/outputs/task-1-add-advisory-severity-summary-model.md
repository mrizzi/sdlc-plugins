## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new advisory-summary endpoint and contains fields for each severity level (critical, high, medium, low) plus a total count. The struct must derive Serialize and any other traits consistent with existing model structs in the SBOM module.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new summary model

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`

## Implementation Notes
- Follow the existing model pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`. Both derive `Serialize` and possibly `Debug`, `Clone`.
- The struct should derive `serde::Serialize` at minimum for JSON response serialization via Axum.
- The response shape must match the requirement: `{ critical: N, high: N, medium: N, low: N, total: N }` — use `serde(rename_all = "camelCase")` or snake_case as consistent with existing endpoint responses (inspect existing model serialization conventions).
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` contains a `severity` field — reference this to understand how severity values are represented in the existing codebase.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct demonstrating the derive macro pattern and serialization conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field type used across the advisory domain

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields for critical, high, medium, low, and total counts
- [ ] Struct derives necessary traits for JSON serialization (at minimum `Serialize`)
- [ ] Struct is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Struct follows the same derive and attribute patterns as sibling model structs

## Test Requirements
- [ ] Verify the struct can be serialized to JSON with the expected field names
- [ ] Verify default/zero values serialize correctly

## Dependencies
- None

[sdlc-workflow] Description digest: sha256:feaf488d080ac49212091e41d7354b80b2ac47903a68dfc5140d643c0a92da2d

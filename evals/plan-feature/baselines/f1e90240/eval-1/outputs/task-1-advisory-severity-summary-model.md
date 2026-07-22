# Task 1: Add advisory severity summary response model

**Jira Parent**: TC-9001
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Repository

trustify-backend

## Target Branch

main

## Description

Define the `AdvisorySeveritySummary` response struct that represents aggregated severity counts for advisories linked to a given SBOM. This struct will be returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The model must include fields for each severity level (critical, high, medium, low) and a total count, all as unsigned integers. It must derive `Serialize` so Axum can return it as JSON.

## Acceptance Criteria

- [ ] `AdvisorySeveritySummary` struct is defined with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives `serde::Serialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI generation
- [ ] Struct is publicly exported from the sbom model module
- [ ] A `SeverityThreshold` enum is defined with variants `Critical`, `High`, `Medium`, `Low` to support the optional threshold query parameter
- [ ] `SeverityThreshold` derives `serde::Deserialize` so it can be parsed from query parameters

## Test Requirements

- [ ] Unit test verifies `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifies `SeverityThreshold` deserializes from lowercase string values

## Files to Create

- `modules/fundamental/src/sbom/model/advisory_summary.rs` -- new module containing `AdvisorySeveritySummary` struct and `SeverityThreshold` enum

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod advisory_summary;` and re-export the public types

## Implementation Notes

- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` which defines `SbomSummary` with serde derives and public fields.
  - Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `model/` scope.
- Use `serde(rename_all = "camelCase")` if the existing models use camelCase serialization, or `snake_case` to match the existing style in `modules/fundamental/src/sbom/model/summary.rs`.

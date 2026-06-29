## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This struct is the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint and contains fields for each severity level (critical, high, medium, low) plus a total count. Additionally, define a `SeverityThreshold` enum to support optional threshold filtering in later tasks.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, and `total` fields (all `i64`), plus `SeverityThreshold` enum with variants `Critical`, `High`, `Medium`, `Low`; derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` to expose the new model module

## Implementation Notes
Follow the existing model struct pattern established in `modules/fundamental/src/sbom/model/summary.rs` (the `SbomSummary` struct). The new struct should derive the same serde traits and be public. The `SeverityThreshold` enum should implement `FromStr` or use `serde` deserialization to parse from query parameters (e.g., `"critical"` -> `SeverityThreshold::Critical`).

Reference `modules/fundamental/src/advisory/model/summary.rs` for how the `AdvisorySummary` struct defines its severity field — the `AdvisorySeveritySummary` aggregation struct groups counts by those same severity values.

Per CONVENTIONS.md §Module pattern: create the model file under `model/` following the `model/ + service/ + endpoints/` structure.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Response types: follow the response struct patterns from `common/src/model/paginated.rs` for serialization traits and field naming.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`
- [ ] `SeverityThreshold` enum is defined with variants `Critical`, `High`, `Medium`, `Low`
- [ ] `SeverityThreshold` can be parsed from lowercase string values
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test that `AdvisorySeveritySummary` serializes to expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test that `SeverityThreshold` parses from string values `"critical"`, `"high"`, `"medium"`, `"low"`
- [ ] Unit test that `SeverityThreshold` returns an error for invalid input like `"unknown"`

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:99f41a17f8731ba0402ac417d43480324cfc01dd581e67eccaae9f76d925d438

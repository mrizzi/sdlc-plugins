## Repository
trustify-backend

## Description
Add an `AdvisorySeveritySummary` response model struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct will be returned by the new advisory-summary endpoint and contains fields for each severity level (critical, high, medium, low) plus a total count. An optional `SeverityThreshold` enum is also needed to support the `?threshold` query parameter for filtering counts above a given severity level.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct and SeverityThreshold enum

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new advisory_summary module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails): derive `Serialize`, `Deserialize`, `Clone`, `Debug` on the struct.
- The `AdvisorySeveritySummary` struct should have fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`.
- The `SeverityThreshold` enum should have variants `Critical`, `High`, `Medium`, `Low` and implement `FromStr` or use `serde` deserialization to parse from the query parameter string.
- Reference the severity field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to ensure the severity level names align with existing domain terminology.
- Per the key conventions: response types follow the pattern in `common/src/model/paginated.rs` — this is a standalone struct (not paginated) but should follow the same derive and serialization conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the derive macros and serialization pattern to follow for response model structs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; use consistent severity level naming

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total (all u64)
- [ ] `SeverityThreshold` enum exists with variants Critical, High, Medium, Low and can be parsed from a lowercase string
- [ ] The new module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] The struct derives Serialize, Deserialize, Clone, Debug

## Test Requirements
- [ ] Unit test that `AdvisorySeveritySummary` serializes to the expected JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test that `SeverityThreshold` parses correctly from strings "critical", "high", "medium", "low"
- [ ] Unit test that `SeverityThreshold` returns an error for invalid input strings

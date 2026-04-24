## Repository
trustify-backend

## Description
Define the AdvisorySeveritySummary response model struct that represents aggregated severity counts for advisories linked to an SBOM. This struct is the foundational data type consumed by both the service layer (Task 2) and the endpoint handler (Task 3). It must serialize to JSON matching the API contract: `{ critical, high, medium, low, total }`.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with fields `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`, deriving Serialize, Deserialize, Clone, Debug, PartialEq, and Default

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration to expose the new model module

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `AdvisorySeveritySummary` as `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` (this task defines the response type only; the endpoint is wired in Task 3)

## Implementation Notes
- Follow the pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definition conventions, derive macros, and module re-exports.
- Use `serde::Serialize` and `serde::Deserialize` derives, consistent with other model structs in the same directory.
- Use `u64` for all count fields to handle large SBOM-advisory sets without overflow.
- Include a `Default` derive so the struct can be initialized with zero counts when an SBOM has no linked advisories.
- Reference `modules/fundamental/src/advisory/model/summary.rs` for how the severity field is represented on AdvisorySummary — the aggregation service (Task 2) will group by this field's values.
- Per constraints (section 5), do not duplicate existing types — reuse the severity representation from the advisory model.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field type/enum that defines valid severity levels; reuse this type for grouping in the aggregation query
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Pattern reference for struct conventions (derives, field types, module registration)

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs`
- [ ] Struct has fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
- [ ] Struct derives Serialize, Deserialize, Clone, Debug, PartialEq, and Default
- [ ] Module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `cargo check -p trustify-module-fundamental` compiles with no errors

## Test Requirements
- [ ] Unit test that constructs an AdvisorySeveritySummary with known values and verifies all fields are accessible
- [ ] Unit test that serializes AdvisorySeveritySummary to JSON and verifies the output matches `{"critical":5,"high":3,"medium":2,"low":1,"total":11}` format
- [ ] Unit test that deserializes a JSON string into AdvisorySeveritySummary and verifies field values
- [ ] Unit test that `Default::default()` produces all-zero counts

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — all unit tests pass

## Dependencies
- Depends on: None

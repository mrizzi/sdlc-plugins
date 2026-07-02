## Repository
trustify-backend

## Target Branch
main

## Description
Define the `AdvisorySeveritySummary` response model struct to represent aggregated advisory severity counts for an SBOM. This struct will serve as the response type for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint, containing counts for each severity level (critical, high, medium, low) plus a total.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New model struct `AdvisorySeveritySummary` with severity count fields and Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` declaration and re-export `AdvisorySeveritySummary`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct layout, derives (`Serialize`, `Deserialize`, `Debug`, `Clone`), and module organization.
- The struct should have five public fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`.
- Use `serde::Serialize` to enable JSON serialization matching the API contract: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.
- Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context() wrapping for any fallible operations. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust language scope.

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct is defined with fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Struct is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Struct can be instantiated and serialized to JSON with expected field names
- [ ] Deserialization from valid JSON produces correct field values

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira

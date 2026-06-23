# Task 1: Add AdvisorySeveritySummary response model

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response struct that represents the severity aggregation result. This struct will be returned by the new advisory summary endpoint and contains counts for each severity level plus a total. This is the foundation that subsequent tasks (service logic, endpoint handler) depend on.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — defines the `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`, deriving `Serialize`, `Deserialize`, `Clone`, `Debug`, and implementing `utoipa::ToSchema` for OpenAPI docs
- `modules/fundamental/src/sbom/model/severity_threshold.rs` — defines a `SeverityThreshold` enum (`Critical`, `High`, `Medium`, `Low`) with `FromStr` / `Deserialize` implementations to parse the `?threshold=` query parameter

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and `pub mod severity_threshold;` declarations to export the new modules

## Implementation Notes
- Follow the struct pattern used in `modules/fundamental/src/sbom/model/summary.rs` for `SbomSummary` -- derive the same trait set and use the same doc-comment style.
- The `AdvisorySeveritySummary` struct does NOT use `PaginatedResults<T>` from `common/src/model/paginated.rs` because it is a single aggregation object, not a list. However, reference that file to see the standard serde/utoipa derive pattern.
- The `SeverityThreshold` enum should match severity levels used in `modules/fundamental/src/advisory/model/summary.rs` where `AdvisorySummary` includes a severity field -- use the same severity level names for consistency.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` directory structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module files scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, derive macros, and serde attributes
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition to ensure consistent severity level naming
- `common/src/model/paginated.rs::PaginatedResults` — reference for standard response struct patterns (derive macros, utoipa integration)

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct compiles with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] Struct derives `Serialize`, `Deserialize`, `Clone`, `Debug`, and implements `ToSchema`
- [ ] `SeverityThreshold` enum has variants `Critical`, `High`, `Medium`, `Low` with case-insensitive deserialization
- [ ] Both types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `AdvisorySeveritySummary` serializes to JSON with expected field names (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Unit test: `SeverityThreshold` parses from lowercase strings ("critical", "high", "medium", "low")
- [ ] Unit test: `SeverityThreshold` returns error for invalid strings

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- None (this is the first task)

---

> [sdlc-workflow] Description digest: sha256-md:a3f1c7b29e4d068531f6a8924b5e7d1c03f9ae82d4b61057c8e3f29a4d7b6e10

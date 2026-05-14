# Task 1 — Add AdvisorySeveritySummary model and SbomService aggregation method

## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model and service layer for advisory severity aggregation. This introduces an `AdvisorySeveritySummary` struct that holds deduplicated severity counts (critical, high, medium, low, total) for a given SBOM, and adds a method to `SbomService` that queries the `sbom_advisory` join table to produce these counts. This task provides the foundation that the endpoint handler (Task 2) will call.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` — New struct `AdvisorySeveritySummary` with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Implements `Serialize` for JSON response.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_severity_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn get_advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries advisory severities via the `sbom_advisory` join table, deduplicates by advisory ID, and counts by severity level

## Implementation Notes
- Follow the existing model pattern established by `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct definition, derive macros, and serde attributes.
- The severity field is already present on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`). Use this as the source for severity classification.
- Use SeaORM query builder to join `entity/src/sbom_advisory.rs` with `entity/src/advisory.rs`, applying `DISTINCT` on advisory ID to deduplicate, then `GROUP BY severity` to count.
- The service method should return `AppError::NotFound` (from `common/src/error.rs`) when the SBOM ID does not exist, consistent with the existing `SbomService::fetch` pattern.
- Use the shared query builder helpers from `common/src/db/query.rs` if applicable for filtering.
- Per `docs/constraints.md` section 5.2: inspect existing code before modifying. Per section 5.4: reuse existing utilities and shared modules.

## Reuse Candidates
- `common/src/error.rs::AppError` — Error enum with `NotFound` variant; use for 404 when SBOM not found
- `entity/src/sbom_advisory.rs` — Existing SBOM-Advisory join table entity; use for the aggregation query join
- `entity/src/advisory.rs` — Advisory entity with severity field; use as the source of severity classification
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for model struct patterns (derive macros, serde attributes)

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] `SbomService` has a `get_advisory_severity_summary` method that returns deduplicated severity counts
- [ ] Method returns `AppError::NotFound` for non-existent SBOM IDs
- [ ] Severity counts are deduplicated by advisory ID (same advisory linked multiple times is counted once)
- [ ] The code compiles without errors

## Test Requirements
- [ ] Unit test verifying `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Unit test verifying the `total` field equals the sum of all severity counts

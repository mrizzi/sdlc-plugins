## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical|high|medium|low` query parameter on the advisory-summary endpoint. When provided, the endpoint returns only severity counts at or above the specified threshold level. This enables alerting integrations to query for critical-only counts without receiving the full severity breakdown.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query<ThresholdParams>` extractor with optional `threshold` field to the handler function
- `modules/fundamental/src/sbom/service/sbom.rs` — Extend `get_advisory_summary` to accept an optional `threshold: Option<String>` parameter and filter severity levels accordingly

## Implementation Notes
- Define a `ThresholdParams` struct with `threshold: Option<String>` and derive `Deserialize` for use with Axum's `Query` extractor. Place this in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` alongside the handler.
- Update the handler signature to include `Query(params): Query<ThresholdParams>` and pass `params.threshold` to `SbomService::get_advisory_summary()`.
- In the service method, implement severity ordering: Critical > High > Medium > Low. When threshold is `"critical"`, return only the critical count (with high, medium, low as 0). When `"high"`, return critical and high. When `"medium"`, return critical, high, and medium. When `"low"`, return all (same as no threshold).
- Recalculate `total` to reflect only the included severity levels after threshold filtering.
- Follow the Query extractor pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` for handling optional query parameters.
- Per CONVENTIONS.md §Error Handling: return Result<T, AppError> with .context() wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust language scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of using Axum `Query` extractor for optional parameters
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Existing handler to extend with the new parameter

## Acceptance Criteria
- [ ] `?threshold=critical` returns only the critical count (high, medium, low are 0)
- [ ] `?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `?threshold=low` returns all severity counts (same as no threshold)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] `total` field reflects only the included severity counts after filtering

## Test Requirements
- [ ] Test: `?threshold=critical` filters to critical-only counts
- [ ] Test: `?threshold=high` includes critical and high counts
- [ ] Test: omitting threshold returns full breakdown
- [ ] Test: invalid threshold value returns 400 Bad Request

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira

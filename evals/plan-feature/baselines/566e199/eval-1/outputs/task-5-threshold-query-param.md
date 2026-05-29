# Task 5 — Add optional threshold query parameter to advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold=<severity>` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response only includes counts for severity levels at or above the specified threshold. Valid threshold values are: `critical`, `high`, `medium`, `low`. The severity ordering is: critical > high > medium > low. For example, `?threshold=high` returns counts for `critical` and `high` only, with `medium` and `low` omitted (or set to zero). This supports alerting integrations that only care about high-severity advisories.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter extraction and filtering logic to the handler
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — add a method or utility to filter severity counts based on a threshold level (if not handled inline in the handler)

## Implementation Notes
- Follow the existing query parameter extraction patterns in the SBOM endpoints. Inspect `modules/fundamental/src/sbom/endpoints/list.rs` for how query parameters are extracted using Axum extractors (e.g., `Query<T>` struct).
- Define a query params struct (e.g., `AdvisorySummaryParams`) with an `Option<String>` or `Option<SeverityThreshold>` field for `threshold`.
- Severity ordering for threshold filtering: critical (highest) > high > medium > low (lowest). When `threshold=high`, include `critical` and `high` counts; set `medium` and `low` to 0.
- Return 400 Bad Request if the `threshold` value is not one of the valid severity levels.
- The `total` field should reflect only the counted (non-zeroed) severities when a threshold is applied.
- The cache key must vary by the `threshold` parameter to avoid serving a filtered response for an unfiltered request (or vice versa). Verify that the `tower-http` cache configuration keys on the full URL including query parameters.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — query parameter extraction pattern using Axum `Query<T>`
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — existing handler to extend with threshold support
- `common/src/db/query.rs` — shared query helpers for parameter parsing patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only `critical` count (with `high`, `medium`, `low` set to 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns `critical` and `high` counts (with `medium`, `low` set to 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns `critical`, `high`, and `medium` counts (with `low` set to 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] `total` field reflects only the severity levels included by the threshold filter
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] Cache varies by query parameter to prevent cross-contamination of filtered and unfiltered responses

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count, other levels are 0
- [ ] Integration test: `?threshold=high` returns critical and high counts, medium and low are 0
- [ ] Integration test: no threshold parameter returns all severity counts (backward compatibility)
- [ ] Integration test: invalid threshold value (e.g., `?threshold=unknown`) returns 400
- [ ] Integration test: verify `total` field reflects only included severity counts

## Verification Commands
- `cargo test --test api` — all integration tests pass including threshold-related tests

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

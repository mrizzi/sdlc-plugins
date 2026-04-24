## Repository
trustify-backend

## Description
Add support for the optional `?threshold=<severity>` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only levels at or above the specified threshold. For example, `?threshold=high` returns counts for critical and high only, with medium and low omitted (or zeroed). This enables alerting integrations to check for advisories above a given severity without processing the full breakdown. This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query<ThresholdParams>` extractor to parse the optional `?threshold` query parameter, pass it to the service method
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — Extend the `advisory_severity_summary` method to accept an optional threshold parameter and filter the aggregation query or post-process the results to exclude severity levels below the threshold

## Implementation Notes
- Define a `ThresholdParams` struct with an `Option<String>` (or an enum type matching severity levels) for the `threshold` query parameter. Use Axum's `Query` extractor, following the pattern of other endpoints that accept query parameters.
- Valid threshold values: `critical`, `high`, `medium`, `low`. If an invalid value is provided, return a 400 Bad Request error.
- Severity ordering for filtering: critical > high > medium > low. When `threshold=high`, include critical and high counts; set medium and low to 0 (or omit them). Recalculate `total` to reflect only the included counts.
- The filtering can be done either at the database query level (adding a WHERE clause on severity) or as a post-processing step on the `AdvisorySeveritySummary` struct. Database-level filtering is preferred for consistency with the p95 < 200ms target.
- Follow the existing query parameter patterns in `modules/fundamental/src/sbom/endpoints/list.rs` or `modules/fundamental/src/advisory/endpoints/list.rs` for how query parameters are extracted and validated.
- Per constraints (section 5.1), keep changes scoped to the advisory-summary endpoint and service — do not modify other endpoints.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Pattern for query parameter extraction using Axum's `Query` extractor
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Severity field type that defines valid severity values; use for validation
- `common/src/db/query.rs` — Query builder helpers that may support filtering by enum values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low are 0), total equals critical count
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts, medium and low are 0
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts, low is 0
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` (no threshold) returns all counts as before
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] `total` field reflects only the included severity counts when threshold is applied

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with total matching
- [ ] Integration test: `?threshold=high` returns critical + high counts with correct total
- [ ] Integration test: no threshold returns all severity counts unchanged
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental advisory_summary` — all tests pass including threshold tests

## Dependencies
- Depends on: Task 3 — Endpoint (the base endpoint must exist before adding the filter)

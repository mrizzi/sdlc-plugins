## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=<severity>` query parameter on the advisory-summary endpoint. When provided, the response includes only counts for severity levels at or above the specified threshold. This supports alerting integrations that only need to know about critical or high-severity advisories (UC-2 in the feature spec).

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- Add an optional `threshold` query parameter (one of: `critical`, `high`, `medium`, `low`). When present, filter the severity counts to include only levels at or above the threshold in the standard ordering: Critical > High > Medium > Low. The `total` field should reflect the sum of the included levels only.
- `modules/fundamental/src/sbom/service/sbom.rs` -- Extend the `advisory_severity_summary` method to accept an optional `Severity` threshold parameter. When provided, the SQL query filters to only count advisories at or above the given severity level.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` -- MODIFY: When `threshold` is provided, response includes only severity levels at or above the threshold. Example: `?threshold=high` returns `{ "critical": N, "high": N, "medium": 0, "low": 0, "total": N }` where medium and low are zeroed out (or omitted).

## Implementation Notes
The severity ordering for threshold filtering is: Critical > High > Medium > Low. When `threshold=high`, include Critical and High counts; zero out Medium and Low. This can be implemented either:
- At the SQL level by adding a `WHERE severity >= threshold` clause (if severity is stored as an ordinal or enum with a defined ordering)
- At the application level by zeroing out fields below the threshold after the full aggregation query

Use Axum's `Query<T>` extractor for the optional query parameter, following the pattern in existing list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs` which use query parameter extraction for filtering and pagination. Define a `AdvisorySummaryQuery` struct with `threshold: Option<Severity>` and derive `Deserialize`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Reference for query parameter extraction pattern with Axum `Query<T>`
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Reference the severity field type/enum used in the advisory domain
- `common/src/db/query.rs` -- Query builder helpers for filtering patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (with high, medium, low zeroed or excluded)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold parameter still returns all counts (backward compatible)
- [ ] `total` reflects the sum of only the included severity levels
- [ ] Invalid threshold values return HTTP 400

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count, total matches
- [ ] Integration test: `?threshold=high` returns critical and high counts, total matches
- [ ] Integration test: no threshold parameter returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo check -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental` -- all tests pass

## Dependencies
- Depends on: Task 3 -- Endpoint with caching (the endpoint must exist before the query parameter can be added)

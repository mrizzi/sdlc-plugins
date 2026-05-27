## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only levels at or above the specified threshold. This enables alerting integrations to efficiently check whether critical (or high/medium/low) advisories exist for a given SBOM without processing the full severity breakdown.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and threshold filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `advisory_severity_summary` method to accept an optional threshold parameter

## Implementation Notes
- The threshold parameter defines a severity floor. The severity hierarchy is: Critical > High > Medium > Low. When `?threshold=critical`, return only the `critical` count (and `total` reflecting that filter). When `?threshold=high`, return `critical` and `high` counts. When `?threshold=medium`, return `critical`, `high`, and `medium`. When `?threshold=low` (or omitted), return all counts (same as no filter).
- Use Axum's `Query` extractor to parse the optional `threshold` query parameter. Define a query parameter struct (e.g., `AdvisorySummaryQuery`) following the patterns used by sibling endpoints that accept query parameters.
- Filtered-out severity levels should be set to zero in the response (not omitted), so the response shape remains consistent: `{ critical: N, high: N, medium: N, low: 0, total: N }`.
- Apply the threshold filter at the service layer in `SbomService::advisory_severity_summary` so that the database query only counts advisories at or above the threshold severity, avoiding fetching unnecessary data.
- Follow the error handling pattern: return 400 Bad Request if the threshold value is not a recognized severity level.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — existing handler to extend with query parameter support
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field enum/type definition to reference for valid threshold values
- `common/src/db/query.rs` — query builder helpers for filtering

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count (other levels set to zero) and total reflecting the filter
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium and low set to zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low set to zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all severity counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] Invalid threshold values return HTTP 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with other levels zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: `?threshold=medium` returns critical, high, and medium counts
- [ ] Integration test: no threshold parameter returns all severity counts
- [ ] Integration test: invalid threshold value returns 400 Bad Request
- [ ] Integration test: threshold parameter combined with non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching

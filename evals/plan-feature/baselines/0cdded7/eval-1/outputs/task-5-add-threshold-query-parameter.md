## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters the severity counts to include only severities at or above the specified threshold. Valid threshold values are: critical, high, medium, low. The severity ordering is: critical > high > medium > low. For example, `?threshold=high` returns counts for critical and high only, with medium, low set to 0 and total reflecting only the filtered counts. This is a non-MVP enhancement that supports alerting integration use cases.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and pass threshold to service method
- `modules/fundamental/src/sbom/service/sbom.rs` — modify `get_advisory_summary` to accept an optional threshold parameter and filter severity counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: add optional `threshold` query parameter; when present, only severity levels at or above the threshold are included in counts

## Implementation Notes
- Define a `Threshold` enum (or use the existing severity enum if one exists) with variants: Critical, High, Medium, Low. Implement `Ord` for the severity ordering: Critical > High > Medium > Low.
- Use Axum's `Query` extractor to parse the optional `threshold` parameter from the query string. Reference existing endpoint handlers that use query parameters — check `modules/fundamental/src/sbom/endpoints/list.rs` for pagination/filtering query parameter patterns.
- The query builder helpers in `common/src/db/query.rs` may provide filtering patterns that can be adapted for threshold filtering.
- The threshold filtering can be applied either at the database level (adding a `WHERE severity >= threshold` clause) or at the application level (zeroing out counts below the threshold after aggregation). Database-level filtering is preferred for consistency and performance.
- When no threshold is provided, behavior is unchanged — return all severity counts.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — query parameter extraction pattern for list endpoints
- `common/src/db/query.rs` — shared filtering query helpers
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field, which may already define a severity enum or type

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low are 0), total reflects filtered count
- [ ] `?threshold=high` returns critical and high counts, medium and low are 0
- [ ] `?threshold=medium` returns critical, high, and medium counts, low is 0
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Omitting the threshold parameter returns all severity counts as before
- [ ] Invalid threshold values return a 400 Bad Request

## Test Requirements
- [ ] Integration test: each valid threshold value returns correctly filtered counts
- [ ] Integration test: no threshold parameter returns all counts
- [ ] Integration test: invalid threshold value returns 400

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint

[sdlc-workflow] Description digest: sha256:a5012d7fa73da741a8e3dc598c5ea7c57c26c7a4105729abfee61d4cf75238aa

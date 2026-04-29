# Task 6 — Add Optional Threshold Query Parameter (Non-MVP)

## Repository
trustify-backend

## Description
Add support for an optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only levels at or above the specified threshold. For example, `?threshold=high` returns counts for Critical and High only, with Medium and Low set to 0. This supports alerting integrations that only care about high-severity advisories.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and threshold filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `advisory_summary` method to accept an optional threshold parameter

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: add optional `threshold` query parameter; accepted values: `critical`, `high`, `medium`, `low`

## Implementation Notes
- The threshold parameter defines a minimum severity level. Severity ordering from highest to lowest: Critical > High > Medium > Low.
- When `threshold=high` is specified, the response should include counts for Critical and High, while Medium and Low should be 0. The `total` field should reflect only the counted severities.
- If the threshold parameter is omitted, behavior is unchanged (all severity counts returned) — backward compatible.
- If an invalid threshold value is provided, return HTTP 400 Bad Request with a descriptive error message.
- Use Axum's query parameter extraction (`Query<T>`) for the threshold parameter. Define a query params struct (e.g., `AdvisorySummaryParams`) with `threshold: Option<String>`.
- Follow the pattern of existing endpoints that accept query parameters — check `modules/fundamental/src/sbom/endpoints/list.rs` and `common/src/db/query.rs` for query parameter handling patterns.
- The threshold filtering can be applied either at the database query level (more efficient) or as a post-query filter on the `AdvisorySeveritySummary` struct (simpler). Prefer database-level filtering for consistency with the performance requirement.
- Per `docs/constraints.md` §5.2: inspect the existing endpoint code before modifying.
- Per `docs/constraints.md` §5.1: changes must be scoped to the files listed.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list endpoint with query parameter handling; reference for Axum `Query<T>` extraction pattern
- `common/src/db/query.rs` — shared query builder helpers; may contain filtering patterns applicable to severity threshold filtering

## Acceptance Criteria
- [ ] `?threshold=critical` returns only Critical count (High, Medium, Low are 0)
- [ ] `?threshold=high` returns Critical and High counts (Medium, Low are 0)
- [ ] `?threshold=medium` returns Critical, High, and Medium counts (Low is 0)
- [ ] `?threshold=low` returns all counts (same as omitting the parameter)
- [ ] Omitting `threshold` parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns HTTP 400 Bad Request
- [ ] `total` field reflects only the severity levels included by the threshold filter

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count for an SBOM with mixed severities
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: omitting threshold returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo test -p trustify-tests --test advisory_summary` — all tests including threshold tests should pass
- `curl -s "http://localhost:8080/api/v2/sbom/{id}/advisory-summary?threshold=critical" | jq .` — should return only critical count (with running server)

## Dependencies
- Depends on: Task 3 — Add Advisory Summary Endpoint with Caching
- Depends on: Task 5 — Add Integration Tests for Advisory Summary Endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response only includes counts for severities at or above the specified threshold. For example, `?threshold=high` returns counts for `critical` and `high` only (with `medium` and `low` omitted or set to zero). The severity hierarchy is: critical > high > medium > low. This supports alerting integrations that only care about severities above a certain level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter extraction and filtering logic to the handler
- `modules/fundamental/src/sbom/service/sbom.rs` — optionally extend `advisory_severity_summary` to accept a threshold parameter, or handle filtering in the endpoint handler after receiving full counts

## Implementation Notes
- Use Axum's `Query<T>` extractor to parse the optional `threshold` parameter. Define a small query params struct (e.g., `AdvisorySummaryParams { threshold: Option<String> }`) following the pattern used by list endpoints with pagination parameters.
- The severity hierarchy for filtering is: `critical` > `high` > `medium` > `low`. When `threshold=high`, zero out or omit `medium` and `low` counts. Recalculate `total` to reflect only the included severities.
- Decide whether to filter at the service layer (more efficient — fewer rows counted) or at the endpoint layer (simpler — just zero out fields after getting full counts). For p95 < 200ms with up to 500 advisories, either approach is acceptable. If filtering at the service layer, pass the threshold to `advisory_severity_summary` and add a `WHERE severity >= threshold` clause to the query.
- Validate that the `threshold` value is one of `critical`, `high`, `medium`, `low`. Return 400 Bad Request for invalid values using the `AppError` pattern from `common/src/error.rs`.
- Reference `common/src/db/query.rs` for any existing query parameter parsing helpers.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the endpoint handler to modify (created in Task 3)
- `common/src/db/query.rs` — shared query helpers for parameter parsing and filtering

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the `critical` count (others zero) and `total` equals `critical`
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns `critical` and `high` counts, `medium` and `low` are zero, `total` equals `critical + high`
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns `critical`, `high`, and `medium` counts, `low` is zero
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] Code compiles without errors (`cargo check`)

## Test Requirements
- [ ] Integration test: call with `?threshold=critical`, verify only critical count is non-zero and total matches
- [ ] Integration test: call with `?threshold=high`, verify critical and high counts, medium and low are zero
- [ ] Integration test: call without threshold, verify all counts are returned (backward compatibility)
- [ ] Integration test: call with invalid threshold value (e.g., `?threshold=extreme`), verify 400 response

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental` — expected: all tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint

[sdlc-workflow] Description digest: sha256:1b291dd4b364b756fdadecd00859ec8e87cbbf781e38d0396ca082527db4cde0

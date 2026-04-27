## Repository
trustify-backend

## Description
Add support for the optional `?threshold` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided (e.g., `?threshold=critical`), the response should only include severity counts at or above the specified threshold level. This is a non-MVP enhancement that enables alerting integrations to filter for high-severity advisories efficiently.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query` extractor for the optional `threshold` parameter and filter logic
- `modules/fundamental/src/sbom/service/sbom.rs` — Extend `advisory_summary` method to accept an optional threshold parameter and filter severity counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — MODIFY: When `threshold` is provided, only severity levels at or above the threshold are included in the response. Valid values: `critical`, `high`, `medium`, `low`. Without the parameter, all severity levels are returned (existing behavior unchanged).

## Implementation Notes
- Define the severity ordering as: Critical > High > Medium > Low. When `?threshold=high` is provided, include only Critical and High counts (severities at or above the threshold).
- Add a query parameter struct (e.g., `AdvisorySummaryQuery`) with an `Option<String>` field for `threshold`. Use Axum's `Query` extractor in the handler — follow the pattern used by list endpoints that accept query parameters, such as `modules/fundamental/src/sbom/endpoints/list.rs`.
- Validate the threshold value against the known severity levels. Return a 400 Bad Request with a descriptive error message if an invalid threshold value is provided.
- Extend the `advisory_summary` method in `modules/fundamental/src/sbom/service/sbom.rs` to accept an optional threshold filter. The filtering can be applied either at the database query level (adding a `WHERE severity IN (...)` clause) or post-query by zeroing out counts below the threshold. Prefer database-level filtering for efficiency.
- When threshold filtering is applied, the `total` field should reflect only the sum of the included severity levels.
- Per the repository's key conventions: query helpers in `common/src/db/query.rs` provide shared filtering patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Demonstrates Axum `Query` extractor usage for list endpoints with filtering parameters.
- `common/src/db/query.rs` — Shared query builder helpers for filtering; may provide reusable filter application patterns.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request with descriptive error message
- [ ] `total` field reflects the sum of only the included severity levels

## Test Requirements
- [ ] Test: `?threshold=critical` returns only critical count, other fields are 0 or omitted, total equals critical
- [ ] Test: `?threshold=high` returns critical + high counts, total equals their sum
- [ ] Test: No threshold parameter returns all severity counts (backward compatibility)
- [ ] Test: Invalid threshold value (e.g., `?threshold=extreme`) returns 400 Bad Request
- [ ] Test: `?threshold=low` returns same result as no threshold

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — all tests including threshold tests pass
- `curl "http://localhost:8080/api/v2/sbom/{id}/advisory-summary?threshold=critical"` — returns filtered response

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint
- Depends on: Task 5 — Integration tests (extend with threshold test cases)

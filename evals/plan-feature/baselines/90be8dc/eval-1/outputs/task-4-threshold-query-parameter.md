## Repository
trustify-backend

## Description
Add support for an optional `?threshold=critical|high|medium|low` query parameter to the advisory-summary endpoint. When provided, the response only includes counts for severity levels at or above the specified threshold (e.g., `?threshold=high` returns only critical and high counts).

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query<ThresholdParams>` extractor to parse the optional `threshold` query parameter and pass it to the service
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — Extend `get_advisory_severity_summary` to accept an optional threshold parameter and filter severity counts accordingly

## Implementation Notes
1. Define a `ThresholdParams` struct with `threshold: Option<String>` (or an enum `SeverityThreshold` with variants `Critical`, `High`, `Medium`, `Low`) in the endpoint handler file. Use `#[derive(Deserialize)]` and Axum's `Query<ThresholdParams>` extractor to parse it from the query string.
2. Define the severity ordering: Critical > High > Medium > Low. When a threshold is specified, zero out counts for severity levels below the threshold and recompute `total` to reflect only the included levels.
3. The filtering can be done either at the query level (add a `WHERE severity IN (...)` clause in the service) or at the application level (set excluded severity fields to 0 after the query). Query-level filtering is preferred for performance.
4. Follow the existing query parameter patterns -- see how `common/src/db/query.rs` handles filtering parameters for reference on query construction patterns.

## Reuse Candidates
- `common/src/db/query.rs` — Query filtering patterns for adding WHERE clauses
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Existing handler to extend with query parameter

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only `critical` count (other fields are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns `critical` and `high` counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns `critical`, `high`, and `medium` counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all severity counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` (no threshold) returns all severity counts
- [ ] `total` field reflects the sum of only the included severity levels
- [ ] Invalid threshold value returns 400 Bad Request

## Verification Commands
- `cargo check -p trustify-fundamental` — Compiles without errors

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint and register route

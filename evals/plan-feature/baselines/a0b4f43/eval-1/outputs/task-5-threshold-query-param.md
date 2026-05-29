## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When `?threshold=critical` is provided, the response filters severity counts to include only severities at or above the specified threshold level. The severity hierarchy is: critical > high > medium > low. For example, `?threshold=high` returns counts for critical and high only, with medium and low omitted (set to 0). This enables alerting integrations to poll for critical-and-above advisories without processing the full severity breakdown.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add query parameter extraction for `threshold` and filtering logic in the handler
- `modules/fundamental/src/sbom/service/sbom.rs` — Extend `advisory_severity_summary` method signature to accept an optional threshold parameter and filter counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — MODIFY: Add optional query parameter `threshold` accepting values `critical`, `high`, `medium`, `low`. When provided, severity counts below the threshold are set to 0 and excluded from the total.

## Implementation Notes
- Follow the query parameter extraction pattern used in existing list endpoints. Check `modules/fundamental/src/sbom/endpoints/list.rs` for how query parameters are extracted using Axum's `Query` extractor with a params struct.
- Define a `ThresholdFilter` struct (or add to an existing query params struct) with an `Option<SeverityLevel>` field for the threshold. Use `serde::Deserialize` for automatic parsing from the query string.
- The severity hierarchy for filtering is: critical (highest) > high > medium > low (lowest). When a threshold is set, only severity levels at or above the threshold should have non-zero counts. The `total` field should reflect the sum of only the included severity levels.
- The filtering can be applied either at the database query level (more efficient — only count matching severities) or at the application level (simpler — compute all counts then zero out those below threshold). The application-level approach is recommended for simplicity unless performance profiling indicates otherwise.
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to listed files (constraint 5.1), follow existing patterns (constraint 5.3).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Demonstrates query parameter extraction pattern with Axum's `Query` extractor
- `common/src/db/query.rs` — Shared query builder helpers that may include filtering utilities applicable to severity filtering
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition with possible enum values

## Acceptance Criteria
- [ ] `?threshold=critical` returns only the critical count (high, medium, low set to 0)
- [ ] `?threshold=high` returns critical and high counts (medium, low set to 0)
- [ ] `?threshold=medium` returns critical, high, and medium counts (low set to 0)
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold values return a 400 Bad Request error
- [ ] The `total` field reflects only the included (non-zeroed) severity counts

## Test Requirements
- [ ] Integration test: endpoint with `?threshold=critical` returns only critical count with others zeroed
- [ ] Integration test: endpoint with `?threshold=high` returns critical and high counts
- [ ] Integration test: endpoint without threshold returns all severity counts (no regression)
- [ ] Integration test: endpoint with invalid threshold value returns 400 Bad Request
- [ ] Integration test: `total` field correctly sums only the non-zeroed severity counts

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

## Repository
trustify-backend

## Description
Add support for the optional `?threshold` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided (e.g., `?threshold=critical`), the response includes counts only for severities at or above the specified threshold, with lower severity counts returned as 0. This enables alerting integrations to efficiently query for critical or high-severity advisories without processing the full severity breakdown. This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `Query<AdvisorySummaryParams>` extractor with optional `threshold` field; pass the threshold value to the service method
- `modules/fundamental/src/sbom/service/sbom.rs` — modify `get_advisory_severity_summary` to accept an optional `threshold: Option<String>` parameter and filter counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — MODIFY: accepts optional query parameter `threshold` with values `critical`, `high`, `medium`, `low`; when set, severity counts below the threshold are returned as 0

## Implementation Notes
- Define an `AdvisorySummaryParams` struct for Axum's `Query` extractor in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`, with a single field `threshold: Option<String>`. Follow the query parameter extraction pattern used by the list endpoint in `modules/fundamental/src/sbom/endpoints/list.rs`.
- Define a `SeverityThreshold` enum (or use a string match) to represent the severity ordering: critical > high > medium > low. Parse the threshold string and validate it; return 400 Bad Request for invalid threshold values.
- In `modules/fundamental/src/sbom/service/sbom.rs`, modify `get_advisory_severity_summary` to accept the threshold parameter. After computing all counts, zero out counts for severity levels below the threshold. Severity ordering: critical (highest) > high > medium > low (lowest).
- Example: `?threshold=high` returns `{ "critical": N, "high": N, "medium": 0, "low": 0, "total": N }` where total equals critical + high.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect the endpoint and service files before modifying; keep changes scoped to threshold logic only.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction with Axum's `Query<T>` extractor
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the handler being modified to add query parameter support
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::get_advisory_severity_summary` — the service method being modified to accept threshold filtering
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — check how severity is represented (enum or string) for consistency

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low are 0), total equals critical count
- [ ] `?threshold=high` returns critical and high counts, medium and low are 0, total equals critical + high
- [ ] `?threshold=medium` returns critical, high, and medium counts, low is 0
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with other levels zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts with medium and low zeroed
- [ ] Integration test: no threshold parameter returns all counts (regression test for backward compatibility)
- [ ] Integration test: invalid threshold value (e.g., `?threshold=invalid`) returns 400

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -- threshold` — threshold-related tests pass

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint

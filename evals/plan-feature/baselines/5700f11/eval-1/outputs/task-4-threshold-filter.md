## Repository
trustify-backend

## Description
Add optional `?threshold=critical|high|medium|low` query parameter support to the advisory-summary endpoint. When provided, the response should only include severity counts at or above the specified threshold level. This enables alerting integrations to query for specific severity levels without fetching all counts.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query` extractor for the optional `threshold` parameter and apply filtering logic to the response
- `modules/fundamental/src/sbom/service/sbom.rs` — Extend `advisory_severity_summary` to accept an optional threshold parameter, or add post-query filtering logic

## Files to Create
- `modules/fundamental/src/sbom/model/severity_threshold.rs` — Define a `SeverityThreshold` enum (`Critical`, `High`, `Medium`, `Low`) with `Deserialize` implementation for query parameter parsing

## Implementation Notes
- Define a `SeverityThreshold` enum in `modules/fundamental/src/sbom/model/severity_threshold.rs` with variants `Critical`, `High`, `Medium`, `Low`. Derive `Deserialize` with `#[serde(rename_all = "lowercase")]` so query parameter values like `?threshold=critical` parse directly.
- In the endpoint handler at `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`, add Axum's `Query` extractor alongside the existing `Path` extractor. Define a `AdvisorySummaryParams` struct with `threshold: Option<SeverityThreshold>`.
- The threshold filter can be applied as post-query filtering on the `AdvisorySeveritySummary` struct: zero out severity fields below the threshold. For example, if `threshold=high`, set `medium` and `low` to 0 and recompute `total`.
- Follow the query parameter pattern used by list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` for how `Query` extractors are structured.
- Register the new model in `modules/fundamental/src/sbom/model/mod.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Pattern for `Query` extractor usage with optional parameters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference severity representation for consistency

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low zeroed), with recalculated total
- [ ] `?threshold=high` returns critical and high counts, medium and low zeroed
- [ ] `?threshold=medium` returns critical, high, and medium counts, low zeroed
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with correct total
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: omitting threshold returns all counts
- [ ] Integration test: invalid threshold value (e.g., `?threshold=unknown`) returns 400

## Dependencies
- Depends on: Task 3 — Endpoint (requires the base advisory-summary endpoint to exist)

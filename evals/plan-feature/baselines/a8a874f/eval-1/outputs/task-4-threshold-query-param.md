# Task 4: Add threshold query parameter to advisory-summary endpoint

## Repository

trustify-backend

## Target Branch

main

## Dependencies

- Task 3 (advisory-summary endpoint)

## Description

Add an optional `?threshold=<severity>` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only levels at or above the specified threshold. For example, `?threshold=high` returns counts for `critical` and `high` only, with `medium` and `low` set to 0. The severity hierarchy is: critical > high > medium > low. This supports alerting integrations that only care about severities above a certain level.

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- add `Query<ThresholdParams>` extractor and filter logic
- `modules/fundamental/src/sbom/service/sbom.rs` -- optionally accept a threshold parameter in `advisory_severity_summary` to push filtering to the query level, or handle in the endpoint layer

## Implementation Notes

- Define a `ThresholdParams` struct with `threshold: Option<String>` that derives `Deserialize` for use as an Axum `Query` extractor. Follow the pattern of query param handling in `modules/fundamental/src/sbom/endpoints/list.rs` if it uses query extractors.
- Valid threshold values are: `critical`, `high`, `medium`, `low`. Return a 400 Bad Request if an invalid value is provided.
- Severity hierarchy for filtering: `critical` (only critical), `high` (critical + high), `medium` (critical + high + medium), `low` (all -- equivalent to no filter).
- When threshold is applied, zero out the counts below the threshold level and recompute `total` to reflect only the included counts.
- The filtering can be done either at the query level (more efficient, filter in SQL WHERE clause) or at the response level (simpler, zero out fields post-query). Prefer the query-level approach for consistency with the performance requirements.

### Applicable Conventions

- **Error handling**: Applies: task modifies `advisory_summary.rs` matching the convention's Rust handler scope -- invalid query params should return `AppError` with appropriate status code.

## Acceptance Criteria

- [ ] `?threshold=critical` returns only critical count, others are 0, total equals critical
- [ ] `?threshold=high` returns critical and high counts, medium and low are 0
- [ ] `?threshold=medium` returns critical, high, and medium counts, low is 0
- [ ] `?threshold=low` returns all counts (same as no threshold)
- [ ] Omitting the parameter returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements

- [ ] Integration test: `?threshold=critical` returns only critical count
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: omitted threshold returns all counts
- [ ] Integration test: invalid threshold value (e.g., `?threshold=extreme`) returns 400

[Description digest: sha256-md:d6a0e5f4c3b2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6 would be posted as a comment]

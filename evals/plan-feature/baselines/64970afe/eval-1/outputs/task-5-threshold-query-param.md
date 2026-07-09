## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When `threshold` is set to a severity level (e.g., `critical`, `high`, `medium`, `low`), the response includes only counts at or above that severity level, with counts below the threshold zeroed out. This enables alerting integrations to query for specific severity thresholds without processing the full breakdown (UC-2 in feature TC-9001). This is a non-MVP requirement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter parsing and response filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `get_advisory_severity_summary` to accept an optional threshold parameter

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — MODIFY: when `threshold` is provided, response includes only severity counts at or above the specified level (counts below are zeroed). Valid values: `critical`, `high`, `medium`, `low`. Invalid values return 400 Bad Request.

## Implementation Notes
- Define a `SeverityLevel` enum with variants `Critical`, `High`, `Medium`, `Low` and `#[derive(Deserialize)]` with `#[serde(rename_all = "lowercase")]` for type-safe query parameter parsing.
- Add a `ThresholdQuery` struct: `pub struct ThresholdQuery { pub threshold: Option<SeverityLevel> }` with `#[derive(Deserialize)]`.
- Update the handler signature to include `Query(query): Query<ThresholdQuery>`.
- Define severity ordering: Critical > High > Medium > Low. When threshold is set, zero out counts below the threshold level in the `SeveritySummary` response.
- Return `AppError::BadRequest` for invalid threshold values that cannot be deserialized into `SeverityLevel`. Axum's `Query` extractor will return a 400 automatically for invalid enum values.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping for fallible operations. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established error handling pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint handler scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — existing endpoint handler to extend with query parameter support
- `modules/fundamental/src/sbom/service/sbom.rs::get_advisory_severity_summary` — existing service method to extend with optional threshold
- `common/src/db/query.rs` — query parameter parsing patterns used in other endpoints (e.g., list endpoints with filtering)

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low zeroed)
- [ ] `?threshold=high` returns critical and high counts (medium, low zeroed)
- [ ] `?threshold=medium` returns critical, high, and medium counts (low zeroed)
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] No threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: verify `?threshold=critical` returns only critical count with others zeroed
- [ ] Integration test: verify `?threshold=high` returns critical and high counts
- [ ] Integration test: verify no threshold returns all counts (backward compatibility)
- [ ] Integration test: verify invalid threshold value (e.g., `?threshold=invalid`) returns 400

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

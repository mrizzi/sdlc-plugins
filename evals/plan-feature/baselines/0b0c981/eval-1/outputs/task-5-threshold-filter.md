## Repository
trustify-backend

## Target Branch
main

## Description
Add optional `?threshold` query parameter support to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When `threshold=critical` is provided, only severity counts at or above the specified threshold are included in the response (e.g., `?threshold=high` returns only critical and high counts). This supports alerting integrations that need to check for advisories above a certain severity level. The severity ordering is: critical > high > medium > low.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add `Query<ThresholdParams>` extractor to the handler function to accept the optional `threshold` query parameter
- `modules/fundamental/src/sbom/service/sbom.rs` — Modify `get_advisory_severity_summary` to accept an optional threshold parameter and filter severity counts accordingly
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Add `ThresholdParam` enum (Critical, High, Medium, Low) for query parameter deserialization, or make severity count fields optional (`Option<u64>`) to represent filtered-out levels

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: Add optional `threshold` query parameter. When provided, only severity levels at or above the threshold are included. Valid values: `critical`, `high`, `medium`, `low`. When omitted, all severity levels are returned (backward compatible).

## Implementation Notes
Follow the existing query parameter extraction pattern in the SBOM list endpoint at `modules/fundamental/src/sbom/endpoints/list.rs`. That file demonstrates how to define a query parameter struct and use Axum's `Query<T>` extractor.

Define a query parameter struct:
```rust
#[derive(Debug, Deserialize)]
pub struct AdvisorySummaryParams {
    pub threshold: Option<String>,  // or Option<SeverityThreshold> with custom Deserialize
}
```

The severity ordering for threshold filtering is: critical > high > medium > low. When `threshold=high` is provided, only `critical` and `high` counts should be non-zero (or present); `medium` and `low` should be zeroed out or omitted.

Two approaches for the response shape:
1. **Zero out filtered levels** — keep all fields present but set filtered-out levels to 0, recalculate `total`. Simpler and backward compatible.
2. **Use `Option<u64>` fields** — set filtered-out levels to `None` (serialized as `null`). More explicit but changes the response shape.

Prefer approach 1 (zero out) for backward compatibility with existing consumers.

Validate the threshold parameter value. If an invalid value is provided, return a 400 Bad Request error using `AppError`.

Per constraints §5.2: inspect the existing query parameter patterns in `list.rs` before implementing.
Per constraints §5.3: follow the query parameter patterns found in those files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Demonstrates query parameter struct definition and `Query<T>` extractor usage in the SBOM module
- `common/src/db/query.rs` — Shared query helpers; reference for filtering parameter patterns
- `common/src/error.rs::AppError` — Use for 400 Bad Request validation errors on invalid threshold values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (other levels zeroed)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low zeroed)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low zeroed)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] Omitting the `threshold` parameter returns all severity counts (backward compatible)
- [ ] Invalid `threshold` value returns 400 Bad Request
- [ ] `total` field reflects only the non-zeroed severity counts when threshold is applied
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with other levels zeroed and correct total
- [ ] Integration test: `?threshold=high` returns critical and high counts with correct total
- [ ] Integration test: omitting `threshold` returns all counts (backward compatibility)
- [ ] Integration test: invalid `threshold` value (e.g., `?threshold=foo`) returns 400
- [ ] Integration test: `total` field equals sum of non-zeroed severity counts

## Verification Commands
- `cargo test -p trustify-tests --test api` — expected: all integration tests pass including threshold scenarios

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint handler


[sdlc-workflow] Description digest: sha256:66440877a527d1e5dec907edddb34959d80a4bcb1b9da6b35746903b65bebb7b

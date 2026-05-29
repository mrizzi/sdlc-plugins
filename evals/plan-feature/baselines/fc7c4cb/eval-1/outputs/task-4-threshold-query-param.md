## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided (e.g., `?threshold=critical`), the response filters severity counts to include only levels at or above the specified threshold. Valid threshold values are: critical, high, medium, low. This enables alerting integrations to query for specific severity levels without processing the full summary.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add Query extractor for optional threshold parameter, apply filtering logic to the response
- `modules/fundamental/src/sbom/service/sbom.rs` — optionally extend the service method to accept a threshold filter parameter, or apply filtering in the endpoint handler

## Implementation Notes
- Use Axum's `Query` extractor to parse optional query parameters. Define a query params struct (e.g., `AdvisorySummaryParams`) with an `Option<String>` or `Option<SeverityThreshold>` field for `threshold`.
- Follow the query parameter extraction pattern used in list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs` — inspect this file for how Axum query parameter structs are defined and extracted.
- The threshold filter determines which severity levels to include in the response. Severity ordering from highest to lowest: critical > high > medium > low. When `?threshold=high`, include critical and high counts; set medium and low to 0 (or omit them).
- Validate the threshold value — return 400 Bad Request for invalid threshold values. Use the existing error handling pattern from `common/src/error.rs`.
- The filtering logic can be applied either in the service layer or in the endpoint handler after receiving the full summary. Prefer the simpler approach: filter in the handler by zeroing out counts below the threshold.
- Ensure the `total` field reflects the filtered counts (sum of only the included severity levels).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for Axum Query extractor pattern with optional parameters
- `common/src/db/query.rs` — shared query helpers; inspect for existing filtering patterns
- `common/src/error.rs::AppError` — reuse for 400 Bad Request error variant

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count (other levels zeroed or omitted), total reflects filtered count
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no filter)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with correct total
- [ ] Integration test: `?threshold=high` returns critical and high counts with correct total
- [ ] Integration test: no threshold parameter returns full summary (backward compatibility)
- [ ] Integration test: invalid threshold value (e.g., `?threshold=unknown`) returns 400

## Dependencies
- Depends on: Task 3 — Add advisory summary endpoint

[sdlc-workflow] Description digest: sha256:0d98db153c07c0cd735d287da7987ec241cb0f4141408c036720b63ad0d7e7a8

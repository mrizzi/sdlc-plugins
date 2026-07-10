**Summary:** Add remediation REST API endpoints
**Issue Type:** Task
**Parent Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Add REST API endpoints for the remediation feature: `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`. These endpoints delegate to the RemediationService created in Task 1 and follow the established endpoint registration and route mounting patterns.

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` — Route registration for /api/v2/remediation/* endpoints
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `modules/fundamental/src/remediation/endpoints/by_product.rs` — GET /api/v2/remediation/by-product handler

## Files to Modify
- `server/src/main.rs` — Mount the remediation module routes alongside existing module mounts
- `modules/fundamental/src/lib.rs` — Export the remediation module

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated vulnerability counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved) as a single JSON object
- `GET /api/v2/remediation/by-product` — NEW: Returns per-product remediation breakdown with total, open, in-progress, and resolved counts. Supports pagination via `offset` and `limit` query parameters.

## Implementation Notes
Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs` and mount in `server/src/main.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md §Response types: the by-product endpoint returns `PaginatedResults<ProductRemediation>` for consistent pagination behavior across all list endpoints.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Caching: use `tower-http` caching middleware for the summary endpoint to meet the p95 < 500ms response time target.
Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Follow the endpoint registration pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`:
- Define routes using Axum's `Router::new().route()` method
- Use `Json()` extractor for responses
- Add tower-http caching middleware configuration for the summary endpoint

The summary endpoint does not require pagination (returns a single aggregation object). The by-product endpoint should support `offset` and `limit` query parameters using `common/src/db/query.rs` helpers.

Mount the remediation routes in `server/src/main.rs` following the same pattern as existing module mounts (see how sbom and advisory modules are mounted).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for domain REST endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — list endpoint handler pattern with PaginatedResults and query parameter extraction
- `common/src/error.rs::AppError` — error type implementing IntoResponse; use for all handler return types
- `common/src/db/query.rs` — query builder helpers for pagination parameter handling

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with severity x status aggregation JSON
- [ ] `GET /api/v2/remediation/by-product` returns 200 with paginated product remediation data
- [ ] Routes are registered in `server/src/main.rs` and accessible via HTTP
- [ ] Summary endpoint includes appropriate caching headers for p95 < 500ms target
- [ ] By-product endpoint supports `offset` and `limit` query parameters

## Test Requirements
- [ ] Verify endpoint registration by calling each endpoint path and asserting 200 status code
- [ ] Verify summary response shape matches the RemediationSummary model struct
- [ ] Verify by-product pagination parameters (offset/limit) produce correct result subsets

## Dependencies
- Depends on: Task 1 — Add remediation domain model and aggregation service

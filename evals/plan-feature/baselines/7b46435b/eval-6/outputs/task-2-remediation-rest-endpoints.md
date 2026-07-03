## Repository
trustify-backend

## Target Branch
main

## Description
Implement the REST API endpoints for remediation tracking. This task creates two new endpoints: `GET /api/v2/remediation/summary` for aggregated severity-status counts and `GET /api/v2/remediation/by-product` for per-product remediation breakdowns. Both endpoints use the `RemediationService` methods created in Task 1 and follow the established Axum endpoint patterns. Caching is applied to the summary endpoint to meet the p95 < 500ms response time target.

Parent Epic: TC-9006: trustify-backend

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Files to Create
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for remediation endpoints, registers both routes
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- `GET /api/v2/remediation/summary` handler returning `RemediationSummary`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- `GET /api/v2/remediation/by-product` handler with pagination query params, returning `PaginatedResults<ProductRemediation>`

## Files to Modify
- `server/src/main.rs` -- mount remediation routes alongside existing module routes (sbom, advisory, package, search)
- `modules/fundamental/src/remediation/mod.rs` -- add `pub mod endpoints;` to register the endpoints sub-module

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns `RemediationSummary` JSON with severity x status counts and totals
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- NEW: returns `PaginatedResults<ProductRemediation>` with per-product breakdown; supports pagination via `offset` and `limit` query parameters

## Implementation Notes
Follow the endpoint pattern established in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration and `modules/fundamental/src/sbom/endpoints/list.rs` for handler implementation.

Each handler should:
- Accept the Axum `State` extractor for the application context (database pool, services)
- Use `Query<PaginationParams>` for the by-product endpoint, following the pattern used in `modules/fundamental/src/sbom/endpoints/list.rs`
- Return `Result<Json<T>, AppError>` following the established error handling pattern
- Apply tower-http caching middleware with a 5-minute TTL for the summary endpoint to meet the p95 < 500ms requirement. Cache configuration follows the approach described in `server/src/main.rs` route builders.

Route registration in `endpoints/mod.rs` should use `Router::new().route(...)` and the routes should be mounted in `server/src/main.rs` alongside existing module mounts.

Per CONVENTIONS.md: endpoint handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task creates `modules/fundamental/src/remediation/endpoints/by_product.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- endpoint route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/list.rs` -- list handler with pagination pattern
- `modules/fundamental/src/sbom/endpoints/get.rs` -- single-item handler pattern for error handling
- `common/src/model/paginated.rs::PaginatedResults<T>` -- paginated response wrapper for by-product endpoint
- `common/src/db/query.rs` -- shared query builder helpers for pagination parameter handling

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns valid `RemediationSummary` JSON
- [ ] `GET /api/v2/remediation/by-product` returns paginated `ProductRemediation` list
- [ ] Routes are registered in `endpoints/mod.rs` and mounted in `server/src/main.rs`
- [ ] Summary endpoint has caching applied (5-minute TTL via tower-http)
- [ ] By-product endpoint respects `offset` and `limit` query parameters
- [ ] Proper error responses returned for edge cases (internal errors)

## Test Requirements
- [ ] Endpoint handlers compile and serve correct response types
- [ ] Pagination parameters are correctly parsed for by-product endpoint
- [ ] Cache headers are present on summary endpoint responses

## Verification Commands
- `cargo build -p trustify-server` -- compiles without errors
- `cargo run` then `curl http://localhost:8080/api/v2/remediation/summary` -- returns valid JSON response

## Dependencies
- Depends on: Task 1 -- Create remediation models and aggregation service

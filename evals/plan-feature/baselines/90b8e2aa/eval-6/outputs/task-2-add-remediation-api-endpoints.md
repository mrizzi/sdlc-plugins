## Repository
trustify-backend

## Target Branch
main

## Description
Add REST API endpoints for the remediation module: `GET /api/v2/remediation/summary` returning aggregated vulnerability counts by severity and status, and `GET /api/v2/remediation/by-product` returning per-product remediation breakdown. Register the remediation routes in the Axum server.

## Files to Create
- `modules/remediation/src/endpoints/mod.rs` — route registration for `/api/v2/remediation` namespace, mounting summary and by-product handlers
- `modules/remediation/src/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`; calls `RemediationService::get_summary()` and returns JSON response
- `modules/remediation/src/endpoints/by_product.rs` — handler for `GET /api/v2/remediation/by-product`; calls `RemediationService::get_by_product()` with optional query parameters for pagination and returns JSON response

## Files to Modify
- `modules/remediation/src/lib.rs` — export the `endpoints` sub-module
- `server/src/main.rs` — mount the remediation module routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns `{ items: RemediationSummary[] }` with severity-by-status aggregation (severity: Critical/High/Medium/Low, status: Open/In Progress/Resolved, count: number)
- `GET /api/v2/remediation/by-product` — NEW: returns `PaginatedResults<ProductRemediation>` with per-product breakdown (product: string, total: number, open: number, in_progress: number, resolved: number)

## Implementation Notes
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Follow the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration.
  Applies: task creates `modules/remediation/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Use this for the by-product endpoint.
  Applies: task creates `modules/remediation/src/endpoints/by_product.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` for the by-product endpoint query parameters.
  Applies: task creates `modules/remediation/src/endpoints/by_product.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Caching: consider using `tower-http` caching middleware for the summary endpoint since aggregation data changes infrequently. See existing endpoint route builders for cache configuration.
  Applies: task creates `modules/remediation/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- All handlers must return `Result<Json<T>, AppError>` following the established error handling pattern.
- Mount remediation routes in `server/src/main.rs` following the same pattern used for `fundamental` and `search` modules.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern for a domain module; reference for how to structure the remediation endpoint module
- `modules/fundamental/src/sbom/endpoints/list.rs` — list endpoint handler pattern with pagination support; reference for the by-product handler
- `common/src/db/query.rs` — shared query builder with filtering and pagination; reuse for by-product query parameter handling
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper; use directly for the by-product endpoint response

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns JSON with severity-by-status aggregation
- [ ] `GET /api/v2/remediation/by-product` returns paginated JSON with per-product breakdown
- [ ] Both endpoints return appropriate HTTP status codes (200 for success, 500 for server errors)
- [ ] Remediation routes are mounted and accessible when the server starts
- [ ] Response shapes match the API contracts specified above

## Test Requirements
- [ ] Verify `GET /api/v2/remediation/summary` returns 200 with correct JSON structure
- [ ] Verify `GET /api/v2/remediation/by-product` returns 200 with paginated response structure
- [ ] Verify both endpoints return empty results gracefully when no data exists

## Verification Commands
- `cargo build -p remediation` — compiles without errors
- `cargo clippy -p remediation` — no warnings

## Documentation Updates
- `README.md` — add remediation endpoints to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Add remediation aggregation models and service

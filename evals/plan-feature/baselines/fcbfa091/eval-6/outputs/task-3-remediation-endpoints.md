## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Create the REST API endpoints for the remediation tracking feature: `GET /api/v2/remediation/summary` for aggregated severity-by-status counts, and `GET /api/v2/remediation/by-product` for per-product remediation breakdown. Register the routes in the Axum server and wire them to the remediation service created in Task 2.

## Files to Create
- `modules/remediation/src/endpoints/mod.rs` — Route registration for `/api/v2/remediation` namespace
- `modules/remediation/src/endpoints/summary.rs` — Handler for `GET /api/v2/remediation/summary`
- `modules/remediation/src/endpoints/by_product.rs` — Handler for `GET /api/v2/remediation/by-product` with query parameters for filtering and pagination

## Files to Modify
- `modules/remediation/src/lib.rs` — Re-export the `endpoints` submodule
- `server/src/main.rs` — Mount the remediation module routes alongside existing modules

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns `RemediationSummary` JSON with severity-by-status aggregated counts
- `GET /api/v2/remediation/by-product` — NEW: Returns `PaginatedResults<ProductRemediation>` JSON with optional query params for pagination (offset, limit) and sorting

## Implementation Notes
Follow the endpoint pattern from `modules/fundamental/src/advisory/endpoints/mod.rs` for route registration and `modules/fundamental/src/advisory/endpoints/list.rs` for handler structure. Each handler extracts query parameters, calls the service method, and returns the result as JSON.

Per CONVENTIONS.md: endpoint registration follows the pattern in each module's `endpoints/mod.rs` which registers routes, and `server/main.rs` mounts all modules.
Applies: task creates `modules/remediation/src/endpoints/mod.rs` and `modules/remediation/src/endpoints/summary.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/remediation/src/endpoints/summary.rs` and `modules/remediation/src/endpoints/by_product.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task creates `modules/remediation/src/endpoints/by_product.rs` matching the convention's `.rs` module scope.

For the summary endpoint:
- No query parameters needed — returns full aggregation
- Returns `Json<RemediationSummary>`

For the by-product endpoint:
- Accept pagination query params via the shared query parameter extractor
- Returns `Json<PaginatedResults<ProductRemediation>>`

In `server/src/main.rs`, add the remediation routes using the same `.merge()` or `.nest()` pattern used for existing modules (sbom, advisory, search).

## Reuse Candidates
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Route registration pattern to follow
- `modules/fundamental/src/advisory/endpoints/list.rs` — Handler pattern for list endpoints with pagination
- `modules/fundamental/src/sbom/endpoints/get.rs` — Handler pattern for single-resource endpoints
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper for the by-product list

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with a valid `RemediationSummary` JSON body
- [ ] `GET /api/v2/remediation/by-product` returns 200 with a valid `PaginatedResults<ProductRemediation>` JSON body
- [ ] By-product endpoint supports pagination via offset/limit query parameters
- [ ] Both endpoints return appropriate error responses (500 with error details) on service failures
- [ ] Routes are mounted in `server/src/main.rs` and accessible when the server starts

## Test Requirements
- [ ] Endpoint returns 200 status for summary request
- [ ] Endpoint returns 200 status for by-product request
- [ ] By-product endpoint respects limit and offset parameters
- [ ] Invalid query parameters return 400 Bad Request

## Verification Commands
- `cargo run` then `curl http://localhost:8080/api/v2/remediation/summary` — Returns JSON with remediation summary
- `cargo run` then `curl http://localhost:8080/api/v2/remediation/by-product?limit=10&offset=0` — Returns paginated product list

## Dependencies
- Depends on: Task 2 — Remediation service

## additional_fields
- labels: ["ai-generated-jira"]
- priority: Major
- fixVersions: ["RHTPA 1.5.0"]

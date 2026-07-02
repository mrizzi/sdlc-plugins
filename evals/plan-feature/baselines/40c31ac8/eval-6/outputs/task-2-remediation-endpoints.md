## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add two new REST endpoints for the remediation tracking dashboard: GET /api/v2/remediation/summary returns aggregated vulnerability counts grouped by severity and status, and GET /api/v2/remediation/by-product returns a paginated per-product remediation breakdown. Register the new routes in the server's route configuration.

## Files to Create
- `modules/fundamental/src/advisory/endpoints/remediation.rs` — Route handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Add `pub mod remediation;` declaration and register remediation routes
- `server/src/main.rs` — Mount the remediation routes alongside existing advisory/SBOM routes

## Implementation Notes
Follow the endpoint registration pattern from existing advisory and SBOM endpoint modules.

- The summary handler calls the `get_remediation_summary()` service method from Task 1 and returns JSON
- The by-product handler calls `get_remediation_by_product()` and wraps results in `PaginatedResults<ProductRemediation>`
- Both handlers accept optional filter query parameters (severity, status, product) parsed using patterns from `common/src/db/query.rs`
- Route registration in `remediation.rs` follows the pattern in `modules/fundamental/src/advisory/endpoints/mod.rs`
- In `server/src/main.rs`, mount the remediation router the same way advisory and SBOM routers are mounted

Per CONVENTIONS.md §Error Handling: return Result<T, AppError>. Applies: task modifies modules/fundamental/src/advisory/endpoints/mod.rs matching the convention's .rs scope.

## Acceptance Criteria
- [ ] GET /api/v2/remediation/summary returns JSON with severity x status count matrix
- [ ] GET /api/v2/remediation/by-product returns paginated JSON with per-product breakdown
- [ ] Both endpoints support optional filtering by severity, status, and product
- [ ] Routes are registered in server/src/main.rs and accessible
- [ ] Endpoints return appropriate HTTP error codes for invalid requests
- [ ] All handlers return `Result<T, AppError>` with contextual error wrapping

## Test Requirements
- [ ] Verify summary endpoint returns correct JSON structure
- [ ] Verify by-product endpoint supports pagination parameters
- [ ] Verify endpoints return 200 OK with valid data

## Dependencies
- Depends on: Task 1 (remediation summary model and service methods must exist)

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira

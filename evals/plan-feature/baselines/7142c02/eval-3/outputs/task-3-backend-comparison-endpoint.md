## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service to the frontend. This endpoint validates the query parameters, calls the comparison service, and returns the structured diff as JSON. It must meet the p95 < 1s response time requirement for SBOMs with up to 2000 packages each.

## Jira Metadata
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/compare` route alongside existing `/api/v2/sbom` routes
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a structured diff between two SBOMs as JSON. Query parameters `left` and `right` are required SBOM IDs. Returns 400 if either parameter is missing or invalid, 404 if either SBOM is not found.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` — see `get.rs` and `list.rs` for Axum handler conventions.
- Define a query params struct (e.g., `CompareParams { left: Uuid, right: Uuid }`) using Axum's `Query` extractor.
- Call `SbomService::compare()` from Task 2 and return the result as `Json<SbomComparison>`.
- Return appropriate HTTP error codes: 400 for missing/invalid parameters, 404 if either SBOM ID doesn't exist (use `AppError` from `common/src/error.rs`).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. Follow the same pattern used for `list.rs` and `get.rs` route registration.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database. Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Pattern for single-resource Axum handler with ID parameter extraction
- `modules/fundamental/src/sbom/endpoints/list.rs` — Pattern for query-parameter-based endpoint
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow
- `common/src/error.rs::AppError` — Error handling for invalid/missing parameters and not-found cases

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the structured diff JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 400 when `left` or `right` is not a valid ID format
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON matches the expected shape with all six diff sections
- [ ] Endpoint is registered and accessible via the SBOM route group

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — verify response contains correct added/removed packages
- [ ] Integration test: compare with missing `left` parameter — verify 400 response
- [ ] Integration test: compare with missing `right` parameter — verify 400 response
- [ ] Integration test: compare with non-existent SBOM ID — verify 404 response
- [ ] Integration test: compare an SBOM with itself — verify empty diff sections
- [ ] Integration test: verify response content type is `application/json`

## Verification Commands
- `cargo test --test api sbom::compare` — runs the comparison endpoint integration tests
- `curl "http://localhost:8080/api/v2/sbom/compare?left={id1}&right={id2}"` — manual endpoint verification

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types and service logic

[sdlc-workflow] Description digest: sha256-md:2fb18dafea9f0c371d2c64583cb4b6477775fb774507a0d5cb23549695a6973b

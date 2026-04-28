## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare` HTTP endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns a structured diff via the comparison service created in Task 1. This wires the service method into the Axum router and registers the route alongside existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` that parses query params and delegates to `SbomService::compare_sboms`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM router alongside existing routes for `/api/v2/sbom`
- `server/src/main.rs` — No changes expected if SBOM routes are already mounted; verify route mounting includes the new sub-route

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` as JSON. Returns 400 if either parameter is missing, 404 if either SBOM does not exist.

## Implementation Notes
Follow the endpoint pattern established by existing SBOM endpoints in `modules/fundamental/src/sbom/endpoints/`.

**Handler structure** — look at `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for the established pattern. The compare handler should:
1. Define a `CompareQuery` struct with `left: String` and `right: String` fields, deriving `serde::Deserialize` and `utoipa::IntoParams`
2. Extract the query params using Axum's `Query<CompareQuery>` extractor
3. Validate that both `left` and `right` are provided and non-empty; return `AppError::BadRequest` if not
4. Call `SbomService::compare_sboms(left, right)` from `modules/fundamental/src/sbom/service/compare.rs`
5. Return `Json(result)` on success

**Route registration** — in `modules/fundamental/src/sbom/endpoints/mod.rs`, add the compare route. Follow the existing route registration pattern where routes are added to the router. Register `/compare` as a GET route pointing to the compare handler. Ensure it is registered before the `/{id}` wildcard route to prevent path conflicts.

**Error handling** — use `Result<Json<SbomComparisonResult>, AppError>` as the return type, consistent with other handlers. The `AppError` enum in `common/src/error.rs` already implements `IntoResponse`.

**OpenAPI documentation** — add `utoipa` attributes to the handler function for automatic OpenAPI spec generation, following the pattern in existing endpoint files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference pattern for single-resource GET handler
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference pattern for query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error response type with `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON when both IDs are valid
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered alongside existing SBOM routes without breaking them
- [ ] Endpoint appears in the generated OpenAPI spec

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with expected diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: existing SBOM endpoints (`GET /api/v2/sbom`, `GET /api/v2/sbom/{id}`) still work after adding the compare route

## Verification Commands
- `cargo test --package tests -- api::sbom` — run SBOM integration tests, expected: all pass
- `cargo build` — ensure compilation succeeds with the new endpoint wired in

## Dependencies
- Depends on: Task 1 — Backend comparison model and service

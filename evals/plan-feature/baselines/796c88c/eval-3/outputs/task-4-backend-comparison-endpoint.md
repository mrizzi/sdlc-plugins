## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that exposes the SBOM comparison service over HTTP. This endpoint accepts `left` and `right` query parameters (SBOM IDs), invokes the comparison service, and returns the structured diff as JSON. This is the API surface that the frontend will consume.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/compare` route alongside existing `/api/v2/sbom` routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns structured diff between two SBOMs as `SbomComparison` JSON

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs`.

Handler implementation:
1. Define a query parameter struct:
   ```rust
   #[derive(Deserialize)]
   pub struct CompareParams {
       pub left: Uuid,
       pub right: Uuid,
   }
   ```
2. Extract `CompareParams` from the query string using Axum's `Query` extractor.
3. Validate that `left != right` (return 400 `AppError` if equal).
4. Call `SbomComparisonService::compare(left, right)`.
5. Return `Json(comparison)` with status 200.

Route registration in `endpoints/mod.rs`:
- Add `.route("/compare", get(compare::handler))` to the existing SBOM router, ensuring it does not conflict with the `/{id}` path parameter route (register `/compare` before `/{id}`).

Error responses:
- 400 if `left` or `right` is missing or if `left == right`
- 404 if either SBOM ID does not exist (propagated from service)
- 500 for internal errors (propagated via `AppError`)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference for handler pattern (extractors, error handling, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern
- `common/src/error.rs::AppError` — Error handling with `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 400 when `left == right`
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered without conflicting with existing SBOM routes
- [ ] Response JSON shape matches the contract from the Figma design context

## Test Requirements
- [ ] Request with valid left and right IDs returns 200 with correct diff structure
- [ ] Request with missing query params returns 400
- [ ] Request with equal left and right returns 400
- [ ] Request with non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 3 — Backend comparison service

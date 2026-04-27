## Repository
trustify-backend

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), invokes `SbomService::compare`, and returns the structured diff as JSON. This endpoint exposes the comparison service logic built in Task 1 as a REST API.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing `/api/v2/sbom` routes
- `server/src/main.rs` — No changes expected if the SBOM module routes are already mounted (verify during implementation)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns a `SbomComparisonResult` JSON response with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs`. Each endpoint file defines an async handler function that:
1. Extracts query/path parameters using Axum extractors
2. Calls the appropriate `SbomService` method
3. Returns `Result<Json<T>, AppError>`

For the comparison endpoint, define a query parameter struct:
```rust
#[derive(Deserialize)]
pub struct CompareQuery {
    pub left: String,
    pub right: String,
}
```

The handler signature should follow the established pattern:
```rust
pub async fn compare(
    Query(params): Query<CompareQuery>,
    service: Extension<SbomService>,
) -> Result<Json<SbomComparisonResult>, AppError> {
    // ...
}
```

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding `.route("/compare", get(compare::compare))` to the existing SBOM router chain. Ensure the `/compare` route is registered before the `/{id}` wildcard route to avoid path conflicts.

Validate that both `left` and `right` parameters are present; return a 400 Bad Request with a descriptive message if either is missing. Use the same `AppError` pattern from `common/src/error.rs` for error responses.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Reference implementation for single-SBOM endpoint handler pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference implementation for query parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern to follow when adding the new route
- `common/src/error.rs::AppError` — Error type for 400/404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body matching the `SbomComparisonResult` schema
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response content type is `application/json`
- [ ] Route does not conflict with existing `/api/v2/sbom/{id}` route

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct JSON structure
- [ ] Integration test: missing `left` parameter returns 400
- [ ] Integration test: missing `right` parameter returns 400
- [ ] Integration test: non-existent left SBOM ID returns 404
- [ ] Integration test: non-existent right SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom::compare` — Run comparison endpoint integration tests, expect all to pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left=ID1&right=ID2"` — Manual verification returns 200 with diff JSON

## Dependencies
- Depends on: Task 1 — Backend comparison model and service

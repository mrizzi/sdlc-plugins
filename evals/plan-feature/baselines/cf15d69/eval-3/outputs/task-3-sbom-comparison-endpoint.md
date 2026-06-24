## Repository
trustify-backend

## Target Branch
main

## Description
Create the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service. This endpoint accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for the comparison endpoint with query parameter extraction

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/compare` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Create the handler in `modules/fundamental/src/sbom/endpoints/compare.rs` following the pattern in existing endpoint files like `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`.

Define a query parameter struct:
```rust
#[derive(Deserialize)]
pub struct CompareParams {
    pub left: Uuid,
    pub right: Uuid,
}
```

The handler function should:
1. Extract `CompareParams` from query string using Axum's `Query` extractor
2. Call `SbomService::compare(left, right, &db).await`
3. Return `Json(result)` on success or propagate `AppError` on failure

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` by adding `.route("/compare", get(compare::compare))` to the existing SBOM router. Place the `/compare` route before the `/{id}` route to avoid path conflicts.

Per Key Conventions (Endpoint registration): Register route in the module's `endpoints/mod.rs`; `server/main.rs` already mounts the SBOM module. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per Key Conventions (Error handling): Handler returns `Result<Json<SbomComparisonResult>, AppError>`. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's handler scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Missing `left` or `right` parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response content type is `application/json`
- [ ] Route is registered in the SBOM module router

## Test Requirements
- [ ] Manual verification with `curl` against a running dev server
- [ ] Formal integration tests are covered in Task 4

## Dependencies
- Depends on: Task 1 — SBOM comparison model types
- Depends on: Task 2 — SBOM comparison service logic

[sdlc-workflow] Description digest: sha256-md:adf587ec0f2b7cc208f9baf7393ef4de8c89cbcfb437011239c7f6e9af1ecde5

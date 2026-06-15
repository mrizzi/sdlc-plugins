# Task 3 — Add SBOM comparison endpoint and integration tests

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM UUIDs) and returns the structured comparison result. Register the new route in the SBOM module's endpoint configuration and add integration tests covering the endpoint's behavior. The endpoint must meet the p95 < 1s latency requirement for SBOMs with up to 2000 packages each.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing SBOM routes
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare`

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/`. The new `compare.rs` file sits alongside `list.rs` and `get.rs`.

**Query parameters struct** (derive `Deserialize`, `IntoParams`):
```rust
#[derive(Deserialize, IntoParams)]
pub struct CompareParams {
    pub left: Uuid,
    pub right: Uuid,
}
```

**Handler function:**
```rust
pub async fn compare_sboms(
    State(service): State<SbomService>,
    Query(params): Query<CompareParams>,
) -> Result<Json<SbomComparisonResult>, AppError> {
    let result = service.compare(params.left, params.right).await?;
    Ok(Json(result))
}
```

**Route registration** in `endpoints/mod.rs`:
- Add `mod compare;` 
- Register route: `.route("/compare", get(compare::compare_sboms))` -- place this BEFORE the `/{id}` route to avoid path conflict with the path parameter

**Integration tests** in `tests/api/sbom.rs`:
- Test successful comparison of two SBOMs with known differences
- Test 404 response when `left` SBOM ID does not exist
- Test 404 response when `right` SBOM ID does not exist
- Test comparison of identical SBOMs returns empty diff
- Use the existing test pattern: `assert_eq!(resp.status(), StatusCode::OK)` and parse response body as `SbomComparisonResult`

Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/sbom.rs` matching the convention's testing scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Comparison route is registered before `/{id}` to avoid path parameter conflict
- [ ] Response JSON shape matches the contract defined in Figma design context (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Test Requirements
- [ ] Integration test: create two SBOMs with different packages, call compare endpoint, verify all diff categories in response
- [ ] Integration test: request with nonexistent left ID returns 404
- [ ] Integration test: request with nonexistent right ID returns 404
- [ ] Integration test: compare SBOM with itself returns empty arrays for all categories

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 2 — Add SBOM comparison model and service

[sdlc-workflow] Description digest: sha256-md:a104b7caa4a0d9345f12aba7dcd8ab63f3fbbe96c0f6bba28166df8fab675886

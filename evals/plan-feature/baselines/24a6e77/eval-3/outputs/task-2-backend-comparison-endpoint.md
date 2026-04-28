# Task 2 — Backend: SBOM comparison endpoint and route registration

## Repository
trustify-backend

## Description
Add the HTTP endpoint handler for `GET /api/v2/sbom/compare` that accepts `left` and `right` query parameters (SBOM IDs), calls the `SbomService::compare` method, and returns the structured diff as JSON. Register the new route in the SBOM endpoint module and add integration tests.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/compare` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns `SbomComparisonDiff` as JSON

## Implementation Notes

### Handler (`compare.rs`)

Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:

1. Define a query parameter struct:
   ```rust
   #[derive(Deserialize)]
   pub struct CompareQuery {
       pub left: String,
       pub right: String,
   }
   ```

2. Define the handler function:
   ```rust
   pub async fn compare(
       Query(params): Query<CompareQuery>,
       State(service): State<SbomService>,
       // ... database connection extraction per existing pattern
   ) -> Result<Json<SbomComparisonDiff>, AppError>
   ```

3. Validate that both `left` and `right` parameters are present and non-empty
4. Call `service.compare(left_id, right_id, &db).await`
5. Return the result as `Json(diff)`

All handlers in this codebase return `Result<T, AppError>` with `.context()` error wrapping (per `common/src/error.rs`).

### Route registration (`endpoints/mod.rs`)

Add the compare route to the existing SBOM router in `modules/fundamental/src/sbom/endpoints/mod.rs`. Follow the pattern used for `list.rs` and `get.rs` routes:
- The route should be `.route("/compare", get(compare::compare))`
- Register it before the `/{id}` catch-all route to avoid path conflicts

### Response format

The response body is the `SbomComparisonDiff` struct serialized as JSON (defined in Task 1). Example:
```json
{
  "added_packages": [{ "name": "pkg-a", "version": "1.0.0", "license": "MIT", "advisory_count": 0 }],
  "removed_packages": [],
  "version_changes": [{ "name": "pkg-b", "left_version": "1.0.0", "right_version": "2.0.0", "direction": "upgrade" }],
  "new_vulnerabilities": [{ "advisory_id": "CVE-2024-001", "severity": "critical", "title": "RCE in pkg-a", "affected_package": "pkg-a" }],
  "resolved_vulnerabilities": [],
  "license_changes": []
}
```

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function signature, state extraction, and error handling pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `common/src/error.rs::AppError` — error type for handler return type

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonDiff` JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Route is registered in the SBOM endpoint module without breaking existing routes
- [ ] Comparison endpoint response time p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify response structure and content
- [ ] Integration test: compare two identical SBOMs, verify all diff sections are empty arrays
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: verify JSON field names match the expected API contract (`added_packages`, `removed_packages`, etc.)

## Verification Commands
- `cargo test --test api sbom::compare` — expected: all comparison endpoint tests pass
- `cargo build` — expected: clean build with no warnings

## Dependencies
- Depends on: Task 1 — Backend: SBOM comparison diff model and service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters, invokes the comparison service to compute the diff, and returns the structured comparison result as JSON. Register the route in the SBOM endpoint module so it is mounted alongside existing SBOM routes.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for the comparison endpoint; extracts `left` and `right` query parameters, calls the comparison service, returns JSON response

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route (`/api/v2/sbom/compare`) alongside existing list and get routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns SbomComparisonResult JSON containing added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for request extraction and response formatting.
  Per CONVENTIONS.md §Endpoint registration: register the new route in `endpoints/mod.rs` following the existing route registration pattern. The route is mounted via `server/src/main.rs` which mounts all modules.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint file scope.
- Define a query parameter struct (e.g., `CompareQuery { left: String, right: String }`) and extract it using Axum's `Query` extractor.
- Call the comparison service from Task 2 (`compare.rs`) to compute the diff.
- Return `Result<Json<SbomComparisonResult>, AppError>` following the existing endpoint pattern.
- Per CONVENTIONS.md §Error handling: use `.context()` wrapping for meaningful error messages (e.g., "SBOM not found" for invalid IDs).
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust file scope.
- The comparison route must be registered before the `/{id}` catch-all route in `endpoints/mod.rs` to avoid path conflicts (Axum matches routes in registration order).
- No caching required for comparison results — each comparison may differ based on SBOM content changes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern with path parameter extraction; follow for handler structure
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration; extend with comparison route
- `common/src/error.rs::AppError` — existing error type with IntoResponse implementation

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON
- [ ] Missing or invalid left/right parameters return appropriate 400 error
- [ ] Non-existent SBOM IDs return appropriate 404 error
- [ ] Response content type is application/json
- [ ] Route is accessible alongside existing /api/v2/sbom endpoints without conflicts

## Test Requirements
- [ ] Test: valid comparison request returns 200 with correctly structured JSON
- [ ] Test: missing left parameter returns 400 error
- [ ] Test: missing right parameter returns 400 error
- [ ] Test: non-existent SBOM ID returns 404 error
- [ ] Test: comparing same SBOM ID for both left and right returns empty diff

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq .` — returns structured comparison JSON

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model types and diff service

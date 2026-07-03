## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint. This endpoint calls the `SbomService::compare_sboms` method created in Task 1 and returns the structured diff as JSON. The endpoint must accept two required query parameters (`left` and `right` as SBOM UUIDs), return 400 if either parameter is missing, and return 404 if either SBOM ID does not exist. The response p95 latency must be under 1 second for SBOMs with up to 2000 packages each per the non-functional requirements.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Critical", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- handler function `compare_sboms` that extracts `left` and `right` SBOM IDs from query parameters, calls the service method, and returns the JSON comparison result

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- add `mod compare;` and register the `/api/v2/sbom/compare` route in the router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns `SbomComparisonResult` JSON with 200 OK
- Returns 400 if `left` or `right` query parameter is missing
- Returns 404 if either SBOM ID does not exist

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for error handling and response structure. For query parameter extraction, use `axum::extract::Query` with a `CompareParams` struct containing `left: Uuid` and `right: Uuid`.

The handler should:
1. Extract `CompareParams { left, right }` from query using `Query(params)`
2. Validate both parameters are present (Axum returns 400 automatically for missing required query params with proper `Query` deserialization)
3. Call `sbom_service.compare_sboms(params.left, params.right).await`
4. On `Ok(result)` return `Json(result)` with status 200
5. On SBOM-not-found error, return 404 via `AppError` (from `common/src/error.rs`)

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes (list.rs, get.rs). Note: the compare route uses query parameters (`/compare?left=&right=`), not path parameters, to avoid conflict with the existing `/{id}` route.

Per CONVENTIONS.md §Endpoint Registration: endpoint registration goes in each module's `endpoints/mod.rs`; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing SBOM GET handler; reuse the same error handling and response pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` -- existing SBOM list handler; reference for query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration pattern to follow for adding the new route
- `common/src/error.rs::AppError` -- error type for 400/404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with JSON body containing all six diff categories
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Endpoint is registered at the correct path and accessible via the server
- [ ] Response Content-Type is application/json

## Test Requirements
- [ ] Handler returns 200 with correct diff structure for two known SBOMs
- [ ] Handler returns 400 for missing query parameters
- [ ] Handler returns 404 for a non-existent SBOM ID
- [ ] Response matches the `SbomComparisonResult` JSON shape

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left={id1}&right={id2}" | jq .` -- returns comparison JSON

## Dependencies
- Depends on: Task 1 -- Create SBOM comparison diff model and service method

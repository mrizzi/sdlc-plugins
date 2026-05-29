## Repository
trustify-backend

## Target Branch
main

## Description
Update the API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. This covers adding the endpoint to the REST API reference with its path, parameters, request/response shapes, error codes, and caching behavior. The documentation should enable API consumers to understand the endpoint's purpose, call it correctly, and interpret the response, as specified in the feature's Documentation Considerations.

## Files to Modify
- `README.md` — Add a brief mention of the advisory-summary endpoint in the API overview section if an endpoint listing exists

## Documentation Updates
- `README.md` — Add the advisory-summary endpoint to any existing API endpoint listing or feature overview section
- OpenAPI schema — Ensure the `utoipa::ToSchema` derive on `AdvisorySeveritySummary` and the endpoint handler's OpenAPI annotations generate correct schema documentation automatically

## Implementation Notes
- The primary API documentation should be auto-generated via `utoipa` annotations on the handler function and response struct. Verify that the `AdvisorySeveritySummary` struct's `ToSchema` derive (added in Task 1) produces the expected OpenAPI schema fields.
- Add `utoipa::path` attribute macro to the advisory-summary endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` to document the endpoint path, parameters, responses, and description in the OpenAPI spec. Follow the pattern used in existing endpoint handlers like `modules/fundamental/src/sbom/endpoints/get.rs`.
- Document the `?threshold` query parameter as optional with allowed values: `critical`, `high`, `medium`, `low`.
- Document the 404 response for non-existent SBOM IDs, consistent with existing SBOM endpoint documentation.
- Document the 5-minute cache behavior so API consumers understand response freshness guarantees.
- Per docs/constraints.md section 4 (Task Template Rules): tasks that change public APIs should include Documentation Updates (constraint 4.9).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Shows the `utoipa::path` annotation pattern for documenting an SBOM endpoint
- `modules/fundamental/src/advisory/endpoints/get.rs` — Another example of OpenAPI endpoint documentation

## Acceptance Criteria
- [ ] The advisory-summary endpoint appears in the auto-generated OpenAPI documentation with correct path, parameters, and response schema
- [ ] The `?threshold` query parameter is documented as optional with valid enum values
- [ ] 404 response is documented for non-existent SBOM IDs
- [ ] README mentions the new endpoint if an API listing section exists
- [ ] Documentation accurately reflects the implemented behavior

## Test Requirements
- [ ] Verify the OpenAPI spec includes the `/api/v2/sbom/{id}/advisory-summary` path after building
- [ ] Verify the response schema in OpenAPI matches the `AdvisorySeveritySummary` struct fields

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
- Depends on: Task 5 — Add threshold query parameter support

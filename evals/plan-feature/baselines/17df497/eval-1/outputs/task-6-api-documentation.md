# Task 6 — Update API documentation for advisory summary endpoint

## Repository
trustify-backend

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error codes, and caching behavior. This ensures API consumers can discover and use the new endpoint.

## Files to Modify
- `README.md` — add the new endpoint to the API endpoint listing if one exists in the README

## Implementation Notes
- Check whether the repository has dedicated API documentation files (e.g., an OpenAPI spec in `docs/`, or a Swagger definition). If an OpenAPI/Swagger file exists, add the new endpoint definition there following the existing endpoint documentation patterns.
- If the project uses inline doc comments or attributes (e.g., `utoipa` for OpenAPI generation in Rust), add the appropriate annotations to the endpoint handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` instead of manually editing a spec file.
- Document:
  - **Path**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Path parameters**: `id` (UUID) — the SBOM identifier
  - **Query parameters**: `threshold` (optional, string, one of: `critical`, `high`, `medium`, `low`) — filter counts to severities at or above this level
  - **Response 200**: `{ "critical": integer, "high": integer, "medium": integer, "low": integer, "total": integer }`
  - **Response 404**: SBOM not found
  - **Caching**: Response is cached for 5 minutes (300 seconds); cache is invalidated when new advisories are linked to the SBOM

## Documentation Updates
- `README.md` — add new endpoint to API reference section if applicable
- API documentation files (if they exist) — add full endpoint specification

## Acceptance Criteria
- [ ] New endpoint is documented with path, parameters, response shape, and error codes
- [ ] Documentation follows the same format as existing endpoint documentation
- [ ] Caching behavior is mentioned in the documentation

## Test Requirements
- [ ] Manual review: documentation accurately reflects the implemented endpoint behavior

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

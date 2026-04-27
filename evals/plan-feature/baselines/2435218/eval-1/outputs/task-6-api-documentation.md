# Task 6 — Update API Documentation for Advisory-Summary Endpoint

## Repository
trustify-backend

## Description
Update the project's API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error responses, and caching behavior. This ensures API consumers can discover and use the new endpoint without reading source code.

## Files to Modify
- `README.md` — add the new endpoint to any existing API reference or endpoint listing section

## Implementation Notes
- Review the existing `README.md` for how other endpoints are documented (e.g., SBOM list/get, advisory list/get). Follow the same format and level of detail.
- Document the following:
  - **Endpoint**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Path parameter**: `id` — SBOM identifier (UUID)
  - **Query parameter** (optional): `threshold` — severity level filter; valid values: `critical`, `high`, `medium`, `low`. When provided, counts below the threshold are zeroed and total is recalculated.
  - **Success response** (200): `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
  - **Error response** (404): SBOM not found
  - **Caching**: Response is cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM
- If the project uses OpenAPI/Swagger specs, update those as well (check for `openapi.yaml`, `swagger.json`, or similar files).
- Per constraints doc section 4.9: this task exists because the feature introduces a new public API endpoint.

## Acceptance Criteria
- [ ] The new advisory-summary endpoint is documented in the project's API reference
- [ ] Documentation includes endpoint path, method, parameters, response shape, and error responses
- [ ] Documentation mentions the 5-minute caching behavior
- [ ] Documentation format matches the style used for existing endpoints

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary Endpoint

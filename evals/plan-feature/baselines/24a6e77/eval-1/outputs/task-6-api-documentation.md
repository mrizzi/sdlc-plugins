# Task 6 — Update API documentation for advisory summary endpoint

## Repository
trustify-backend

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. This ensures API consumers can discover the endpoint, understand its parameters, and parse its response shape. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters, response schema, error responses, and caching behavior.

## Files to Modify
- `README.md` — add the new endpoint to the API endpoint listing if one exists in the README

## Implementation Notes
- Check whether the project uses OpenAPI/Swagger auto-generation from `utoipa` annotations — if so, the `ToSchema` derive on `AdvisorySeveritySummary` (Task 1) and endpoint annotations (Task 3) may auto-generate most of the API docs, and this task focuses on any supplementary documentation
- If there is a manually maintained API reference section in `README.md` or a `docs/` directory, add the new endpoint there following the existing documentation format and style
- Document the endpoint including:
  - Path: `GET /api/v2/sbom/{id}/advisory-summary`
  - Path parameter: `id` (UUID) — the SBOM identifier
  - Query parameter: `threshold` (optional, enum: `critical`, `high`, `medium`, `low`) — filter to severities at or above this level
  - Response (200): `{ "critical": number, "high": number, "medium": number, "low": number, "total": number }`
  - Error (404): SBOM not found
  - Error (400): invalid threshold value
  - Caching: responses are cached for 5 minutes; cache is invalidated when new advisories are linked to the SBOM
- Per constraints (Section 4.9): include documentation updates when task changes public APIs

## Acceptance Criteria
- [ ] New endpoint is documented with path, method, parameters, response shape, and error codes
- [ ] Documentation follows the existing API documentation format and style in the repository
- [ ] Caching behavior is mentioned in the endpoint documentation

## Test Requirements
- [ ] Documentation review: verify all documented field names match the actual `AdvisorySeveritySummary` struct fields

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

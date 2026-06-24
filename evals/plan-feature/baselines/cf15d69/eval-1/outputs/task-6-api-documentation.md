## Repository
trustify-backend

## Target Branch
main

## Description
Update the API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. This ensures API consumers can discover the endpoint path, query parameters, response shape, and caching behavior. The OpenAPI schema is auto-generated from `utoipa::ToSchema` derives, but the README and any hand-written API reference must also be updated.

## Files to Modify
- `README.md` — Add the new endpoint to the API endpoints listing/table if one exists
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Ensure `#[utoipa::path]` macro is applied to the handler for OpenAPI spec generation

## Implementation Notes
The `utoipa::path` macro should be applied to the handler function in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` following the same pattern used in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`. The macro should document:
- Path: `/api/v2/sbom/{id}/advisory-summary`
- Method: GET
- Path parameter: `id` (UUID)
- Query parameter: `threshold` (optional, enum: critical/high/medium/low)
- Success response: 200 with `AdvisorySeveritySummary` body
- Error response: 404 when SBOM not found

Update `README.md` to mention the new advisory-summary endpoint in the API surface description, consistent with how existing endpoints are documented.

Per Key Conventions (Framework): Axum for HTTP with utoipa for OpenAPI generation. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` files scope.

## Acceptance Criteria
- [ ] `#[utoipa::path]` macro is correctly applied to the advisory-summary handler
- [ ] OpenAPI spec generation includes the new endpoint with correct path, parameters, and response schema
- [ ] `README.md` references the new endpoint
- [ ] Documentation accurately describes the `threshold` query parameter as optional

## Test Requirements
- [ ] Verify OpenAPI spec output includes `/api/v2/sbom/{id}/advisory-summary` path with correct schema

## Verification Commands
- `cargo doc --no-deps -p trustify-fundamental` — documentation builds without warnings
- `cargo check -p trustify-fundamental` — utoipa macros compile correctly

## Dependencies
- Depends on: Task 3 — advisory summary endpoint (handler must exist before adding utoipa macros)

[sdlc-workflow] Description digest: sha256-md:5af8bd2d73e6731f5ecc3dfcc781faf38399829464b33c8ef7b5ace00e4fe294

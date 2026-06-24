## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/license-report` HTTP endpoint that invokes the license report service and returns the compliance report as JSON. Register the new route within the existing SBOM endpoint module.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `server/src/main.rs` — Verify the SBOM module routes are already mounted (likely no change needed since routes are registered via the module's `endpoints/mod.rs`)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that loads the license policy, calls `LicenseReportService::generate_report`, and returns the `LicenseReport` as JSON

## API Changes
- **New endpoint**: `GET /api/v2/sbom/{id}/license-report`
- **Path parameter**: `id` — the SBOM identifier
- **Response (200 OK)**:
  ```json
  {
    "groups": [
      {
        "license": "MIT",
        "packages": [
          { "name": "serde", "version": "1.0.197" }
        ],
        "compliant": true
      },
      {
        "license": "GPL-3.0-only",
        "packages": [
          { "name": "some-gpl-lib", "version": "2.1.0" }
        ],
        "compliant": false
      }
    ]
  }
  ```
- **Response (404)**: SBOM not found
- **Response (500)**: Internal error during report generation

## Implementation Notes
- The handler should extract the SBOM `id` from the path, load `LicensePolicyConfig` from the `license-policy.json` file (or from application state if pre-loaded at startup), and invoke the service.
- Per Key Conventions (Error handling): The handler must return `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping on all fallible calls, matching the pattern in `common/src/error.rs`. Applies: task creates a handler in `modules/fundamental/src/sbom/endpoints/` matching the convention's error handling scope.
- Per Key Conventions (Endpoint registration): Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for `list.rs` and `get.rs`. Applies: task modifies `endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per Key Conventions (Response types): This endpoint returns a single `LicenseReport` object, not a paginated list, so `PaginatedResults<T>` from `common/src/model/paginated.rs` is not needed. Applies: task creates a new endpoint response matching the convention's response types scope.
- Per Key Conventions (Caching): Consider adding `tower-http` caching middleware for this endpoint since license reports for a given SBOM are deterministic (same SBOM + same policy = same report). Applies: task creates a new route that may benefit from caching matching the convention's caching scope.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a 200 response with the `LicenseReport` JSON shape
- [ ] Returns 404 when the SBOM ID does not exist
- [ ] Returns proper error responses for internal failures
- [ ] The route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] The endpoint is accessible through the server's route tree

## Test Requirements
- [ ] Integration test: call the endpoint with a valid SBOM ID that has packages with known licenses; verify the response shape and compliance flags
- [ ] Integration test: call the endpoint with a non-existent SBOM ID; verify 404 response
- [ ] Integration test: call the endpoint with an SBOM that has no packages; verify empty groups array

[sdlc-workflow] Description digest: sha256-md:308866c1614db7fb5791898653f3de12573277c6c72db7b1750204b364460633

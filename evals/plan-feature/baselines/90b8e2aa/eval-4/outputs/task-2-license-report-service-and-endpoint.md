## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service method and HTTP endpoint. The service method aggregates all packages in an SBOM by license type, walks the transitive dependency tree to include indirect dependencies, and checks each license group against the configured policy. The endpoint exposes this as `GET /api/v2/sbom/{id}/license-report` and registers the route in the SBOM module's route configuration.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that calls the service method and returns JSON

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `license_report` method to SbomService that queries package-license data, walks transitive dependencies, groups by license, and checks compliance
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route and add `mod license_report;`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `LicenseReportSummary` JSON with packages grouped by license and compliance flags. Response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract path parameters, call service method, return `Result<Json<T>, AppError>`.
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService::fetch, SbomService::list) for the service method signature and database interaction.
- The service method should:
  1. Query `sbom_package` join table to get all packages for the SBOM.
  2. For each package, query `package_license` entity to get license information.
  3. Walk the dependency tree using the `sbom_package` relationships to include transitive dependencies.
  4. Group packages by license identifier.
  5. Load the `LicensePolicy` configuration and check each group's compliance.
  6. Return `LicenseReportSummary` with the grouped results.
- Use the existing `entity/package_license.rs` entity for querying license data — do not create new entities or tables.
- Use the existing `entity/sbom_package.rs` entity for SBOM-package relationships and dependency walking.
- The handler must return `Result<Json<LicenseReportSummary>, AppError>` and use `.context()` for error wrapping per the project's error handling convention.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Consider batching database queries (load all packages and licenses in bulk rather than N+1 queries).
- Per CONVENTIONS.md Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md Key Conventions (Endpoint registration): register the new route in `endpoints/mod.rs` following the existing route registration pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md Key Conventions (Module pattern): place the endpoint handler in `endpoints/` and service logic in `service/` following the `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's module pattern scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET handler pattern for SBOM detail; follow same structure for license report handler
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; add the license_report method here
- `entity/package_license.rs` — existing Package-License mapping entity for querying license data
- `entity/sbom_package.rs` — existing SBOM-Package join table entity for dependency tree walking
- `common/src/error.rs::AppError` — error type for handler return values
- `common/src/db/query.rs` — shared query builder helpers for efficient database access

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns a JSON response with packages grouped by license type
- [ ] Each license group includes a `compliant` flag based on the configured license policy
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Non-existent SBOM ID returns an appropriate error response (404)
- [ ] Response time is under 500ms (p95) for SBOMs with up to 1000 packages
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Integration test: GET license report for an SBOM with known packages returns correct license groupings
- [ ] Integration test: GET license report flags non-compliant licenses when policy denies them
- [ ] Integration test: GET license report includes transitive dependency packages
- [ ] Integration test: GET license report for non-existent SBOM returns 404
- [ ] Integration test: GET license report for SBOM with no packages returns empty groups array

## Verification Commands
- `cargo test --test api license_report` — all license report integration tests pass
- `cargo clippy --all-targets` — no warnings on new code

## Documentation Updates
- `README.md` — add section documenting the `GET /api/v2/sbom/{id}/license-report` endpoint, its response shape, and license policy configuration (JSON config file format and location)

## Dependencies
- Depends on: Task 1 — Add license report model types and license policy configuration

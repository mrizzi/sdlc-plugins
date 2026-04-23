## Repository
trustify-backend

## Description
Implement the `LicenseReportService` that queries the database for all packages belonging to an SBOM (including transitive dependencies), groups them by license, and applies the license policy to produce a `LicenseReport`. This service is the core business logic layer between the database entities and the HTTP endpoint.

## Files to Create
- `modules/fundamental/src/sbom/license_report/service.rs` -- implements `LicenseReportService` with a `generate_report(sbom_id, db, policy)` method that queries packages, groups by license, evaluates compliance, and returns a `LicenseReport`

## Files to Modify
- `modules/fundamental/src/sbom/license_report/mod.rs` -- add `pub mod service;` declaration

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) -- accept a database connection reference and return `Result<T, AppError>`.
- Use the `sbom_package` entity (`entity/src/sbom_package.rs`) to find all packages linked to the given SBOM ID. This join table maps SBOMs to their constituent packages.
- Use the `package_license` entity (`entity/src/package_license.rs`) to resolve each package's license. This entity maps packages to their declared licenses.
- For transitive dependency traversal: query all `sbom_package` rows for the given SBOM ID. The SBOM ingestion process in `modules/ingestor/src/graph/sbom/mod.rs` already flattens the dependency tree into `sbom_package` entries, so a single query on `sbom_package` for the SBOM ID captures both direct and transitive dependencies.
- Use `common/src/db/query.rs` query builder helpers if additional filtering is needed.
- Group packages by their license string using a `HashMap<String, Vec<PackageSummary>>`, then map each group into a `LicenseGroup` with the compliance flag from `LicensePolicy::evaluate`.
- Wrap database errors with `.context()` as per `common/src/error.rs::AppError` conventions.
- For performance (p95 < 500ms for 1000 packages): use a single joined query rather than N+1 queries. Join `sbom_package` with `package_license` in one SeaORM select.

## Reuse Candidates
- `entity/src/sbom_package.rs` -- SeaORM entity for the SBOM-to-package join table
- `entity/src/package_license.rs` -- SeaORM entity for the package-to-license mapping
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service method signature patterns and DB connection handling
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- error type for `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a `compliant` flag that matches the policy evaluation
- [ ] Transitive dependencies are included (all `sbom_package` entries for the SBOM)
- [ ] The query uses a join (not N+1) for performance
- [ ] Returns `AppError` for invalid/missing SBOM IDs
- [ ] The overall `LicenseReport` has an aggregate `compliant` flag (false if any group is non-compliant)

## Test Requirements
- [ ] Unit test with mock data: service groups 5 packages with 3 distinct licenses into 3 `LicenseGroup` entries
- [ ] Unit test: service correctly marks a group as non-compliant when the license is in the denied list
- [ ] Unit test: service returns an error when the SBOM ID does not exist
- [ ] Unit test: service handles an SBOM with zero packages (returns empty report, compliant = true)
- [ ] Unit test: transitive dependencies are included by verifying all sbom_package entries appear in the report

## Dependencies
- Depends on: Task 1 -- License report model and policy (provides `LicenseReport`, `LicenseGroup`, `LicensePolicy`)

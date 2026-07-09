## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service for TC-9004. This service aggregates package license data from existing database entities (sbom_package and package_license), walks the full transitive dependency tree for a given SBOM, groups packages by license type, and checks each group against the loaded license policy to determine compliance status. The service must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages and must not introduce new database tables — it aggregates from existing package-license data only.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods to generate a compliance report for a given SBOM ID

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` to export the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for struct layout, database connection handling, and error propagation.
- Use SeaORM queries against the existing `sbom_package` and `package_license` entities to retrieve all packages and their licenses for the given SBOM. Do not create new database tables or migrations.
- Implement transitive dependency resolution by walking the SBOM's package dependency graph. Query `sbom_package` join table to build the full dependency tree, then collect all unique packages and their licenses.
- Group packages by license identifier (SPDX format), constructing `LicenseGroup` instances from the model created in Task 1.
- Load the `LicensePolicy` configuration (from Task 1) and use it to set the `compliant` flag on each group.
- Optimize for the p95 < 500ms target: use batch queries rather than N+1 patterns, fetch all package-license mappings in a single query where possible.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure for the sbom module.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on database and policy loading errors.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM service; follow its pattern for database access, connection pooling, and error handling
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for efficient package-license data retrieval
- `entity/src/sbom_package.rs` — SBOM-Package join table entity; use for resolving packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity; use for retrieving license data per package
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service; reference for package data access patterns

## Acceptance Criteria
- [ ] `LicenseReportService` generates a `LicenseReport` for a given SBOM ID
- [ ] All packages (including transitive dependencies) are included in the report
- [ ] Packages are correctly grouped by license identifier
- [ ] Each group's `compliant` flag reflects the loaded license policy
- [ ] No new database tables or migrations are introduced
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test that the service groups packages by license correctly (3+ licenses, multiple packages per license)
- [ ] Unit test that transitive dependencies are included in the license report
- [ ] Unit test that compliance flags are set correctly based on a test policy (mix of approved and denied licenses)
- [ ] Unit test that an SBOM with no packages returns an empty groups array

## Dependencies
- Depends on: Task 1 — Define license compliance report model and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add the license report service that aggregates package license data for a given SBOM,
walks the transitive dependency tree, groups packages by license type, and checks each
group's compliance against the configured license policy. This service queries existing
`package_license` and `sbom_package` entity tables — no new database tables are needed.
The service must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` with a `generate_report(sbom_id, db, policy)` method that returns `Result<LicenseReport, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` and re-export the service

## Implementation Notes
The service should:
1. Query `sbom_package` to get all packages associated with the given SBOM ID
2. For each package, query `package_license` to get its license(s)
3. Walk transitive dependencies by following the package dependency graph through
   `sbom_package` relationships
4. Group all discovered packages by their license identifier
5. For each group, check compliance using `LicensePolicy::is_compliant()`
6. Return a `LicenseReport` with the grouped results

Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs`
(`SbomService`) for method signatures, error handling, and database interaction patterns.
Use the `db` connection pattern established there.

Use the query helpers from `common/src/db/query.rs` for efficient database queries.
Avoid N+1 query patterns — batch-load package licenses where possible.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with
`.context()` wrapping for database query errors.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` directory
structure.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's module directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service pattern (method signatures, database interaction, error handling) for SBOM-related operations
- `modules/fundamental/src/package/service/mod.rs::PackageService` — demonstrates how to query package entities and their relationships
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for efficient license data aggregation
- `entity/src/package_license.rs` — the SeaORM entity for the package-license mapping table; use for license lookups
- `entity/src/sbom_package.rs` — the SeaORM entity for the SBOM-package join table; use for package discovery

## Acceptance Criteria
- [ ] `generate_report()` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each license group has a correct `compliant` flag based on the loaded policy
- [ ] Returns `AppError` when the SBOM ID does not exist
- [ ] No new database tables or migrations are created
- [ ] Report generation meets p95 < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test verifying packages are correctly grouped by license type
- [ ] Unit test verifying transitive dependencies are included in license groups
- [ ] Unit test verifying compliance flags are set correctly for denied licenses
- [ ] Unit test verifying compliance flags are set correctly for allowed licenses
- [ ] Unit test verifying error handling when SBOM ID does not exist
- [ ] Unit test verifying performance with a large package set (benchmark or assertion on query count)

## Dependencies
- Depends on: Task 1 — Add license report model types
- Depends on: Task 2 — Add license policy configuration

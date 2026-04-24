# Task 2 — Add license report service with transitive dependency resolution

## Repository
trustify-backend

## Description
Implement a `LicenseReportService` that generates a license compliance report for a given SBOM. The service aggregates license data from existing package-license records, walks the full transitive dependency tree via the SBOM-package join table, groups packages by license type, and evaluates each group against the license policy (Task 1). No new database tables are required — the service queries existing `package_license` and `sbom_package` entities.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id, db, policy) -> Result<LicenseReport, AppError>` method that queries packages for the SBOM, resolves transitive dependencies, groups by license, and checks compliance
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport` and `LicenseGroup` response structs: `LicenseReport { groups: Vec<LicenseGroup> }`, `LicenseGroup { license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new response model

## API Changes
- Internal service API: `LicenseReportService::generate_report(sbom_id: Uuid, db: &DatabaseConnection, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` — NEW

## Implementation Notes
- Follow the service pattern established by `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` for database access patterns, error handling with `.context()`, and struct organization
- Use SeaORM queries against the existing `package_license` entity (`entity/src/package_license.rs`) joined with `sbom_package` (`entity/src/sbom_package.rs`) to retrieve all packages and their licenses for a given SBOM
- For transitive dependency resolution: query `sbom_package` to get direct packages, then recursively (or iteratively) resolve their dependencies through the package relationship graph. Use a visited set to avoid cycles
- Group results by license identifier, create a `LicenseGroup` for each unique license, and set `compliant` based on `LicensePolicy::is_compliant()`
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single batch query where possible rather than N+1 queries. Consider collecting all package IDs first, then batch-loading their licenses
- Per constraints doc section 5.4: reuse `common/src/db/query.rs` query helpers for any filtering or pagination needs
- Per constraints doc section 5.2: inspect `SbomService` implementation before coding to match its patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Reference implementation for service patterns, DB access, and error handling
- `common/src/db/query.rs` — Shared query builder helpers for filtering
- `common/src/error.rs::AppError` — Error type with `.context()` pattern
- `entity/src/package_license.rs` — Existing entity for package-license mappings
- `entity/src/sbom_package.rs` — Existing entity for SBOM-package relationships
- `entity/src/package.rs` — Package entity with license field
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Includes license field, reference for package data shape

## Acceptance Criteria
- [ ] `generate_report()` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each `LicenseGroup` has a `compliant` flag based on the license policy
- [ ] Returns appropriate error for non-existent SBOM IDs
- [ ] No new database tables are created — only existing entities are queried
- [ ] Performance: report generation completes within 500ms for SBOMs with 1000 packages

## Test Requirements
- [ ] Unit test: service correctly groups packages by license
- [ ] Unit test: transitive dependencies are resolved and included
- [ ] Unit test: compliance flags are set correctly based on policy
- [ ] Unit test: non-existent SBOM ID returns appropriate error
- [ ] Unit test: empty SBOM (no packages) returns an empty groups list
- [ ] Unit test: circular dependency in package graph does not cause infinite loop

## Dependencies
- Depends on: Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the LicenseReport model structs and a LicenseReportService within the sbom module. The service aggregates package-license data from the existing `package_license` entity, walks transitive dependencies via the `sbom_package` join table, groups packages by license, and evaluates compliance against the LicensePolicy (from Task 1). This is the core business logic that the endpoint (Task 3) will expose.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReportGroup and LicenseReport response structs
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with generate_report method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service
- `modules/fundamental/Cargo.toml` — Add dependency on `common` crate if not already present (for LicensePolicy)

## Implementation Notes
Follow the existing module pattern established by `modules/fundamental/src/sbom/service/sbom.rs` for service implementation. The SbomService in that file demonstrates the pattern for database queries, error handling, and result construction.

The LicenseReport struct should contain:
- `groups: Vec<LicenseReportGroup>` — packages grouped by license identifier

Each LicenseReportGroup should contain:
- `license: String` — SPDX license identifier
- `packages: Vec<PackageSummary>` — list of packages with this license (reuse existing PackageSummary from `modules/fundamental/src/package/model/summary.rs`)
- `compliant: bool` — whether this license is compliant per the loaded policy

The service must:
1. Query all packages linked to the given SBOM via `sbom_package` join table
2. Resolve each package's license via `package_license` entity
3. Walk transitive dependencies (packages that depend on other packages within the SBOM)
4. Group packages by license identifier
5. Evaluate each group's compliance against the LicensePolicy
6. Return the assembled LicenseReport

Use SeaORM query patterns consistent with existing service methods. Use `query.rs` helpers from `common/src/db/query.rs` for any filtering or pagination needs.

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batching database queries rather than N+1 patterns when walking the dependency tree.

Per CONVENTIONS.md §Key Conventions: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Key Conventions: use SeaORM for database access.
Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Reference for service method patterns (database queries, error handling, result construction)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Reuse directly as the package type within LicenseReportGroup instead of creating a duplicate struct
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reference for package query patterns
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type for all service method returns
- `entity/src/package_license.rs` — Package-License mapping entity for license lookups
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for dependency resolution

## Acceptance Criteria
- [ ] LicenseReport struct contains groups of packages organized by license identifier
- [ ] Each group includes a compliant boolean evaluated against the LicensePolicy
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] The service correctly handles SBOMs with no packages (returns empty groups)
- [ ] The service correctly handles packages with no license data (grouped under "Unknown" or similar)
- [ ] Performance: report generation completes within 500ms for an SBOM with 1000 packages

## Test Requirements
- [ ] Unit test: generate report for an SBOM with packages under allowed licenses — all groups show compliant: true
- [ ] Unit test: generate report for an SBOM with packages under denied licenses — affected groups show compliant: false
- [ ] Unit test: generate report for an SBOM with mixed compliant and non-compliant licenses
- [ ] Unit test: generate report for an SBOM with transitive dependencies — verify transitive packages appear in the report
- [ ] Unit test: generate report for an SBOM with no packages — returns empty groups list
- [ ] Unit test: packages with no license data are handled gracefully

## Dependencies
- Depends on: Task 1 — Add license policy configuration model

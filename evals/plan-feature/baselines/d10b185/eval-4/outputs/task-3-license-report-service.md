# Task 3 — Add LicenseReportService for compliance report generation

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that generates a license compliance report for a given SBOM. The service aggregates package license data from the database, walks the transitive dependency tree, groups packages by license, and evaluates each group against the loaded license policy to produce a complete `LicenseReport`.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id)` method that queries package-license data, walks transitive dependencies, groups by license, and evaluates compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add module declaration for `license_report`

## Implementation Notes
- Follow the service pattern from `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) — the service should accept a database connection and the `LicensePolicy` as constructor parameters.
- Use the `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch package data, or query directly using SeaORM entities.
- Key SeaORM entities to query:
  - `entity/src/sbom_package.rs` — the SBOM-to-package join table; use to find all packages in an SBOM
  - `entity/src/package_license.rs` — the package-to-license mapping; use to look up the license for each package
  - `entity/src/package.rs` — the package entity with name and version
- For transitive dependency walking: query `sbom_package` for all packages linked to the SBOM (both direct and transitive). If the entity distinguishes direct from transitive dependencies, use that flag; otherwise, include all packages and mark `transitive: false` as a default.
- Use the query helpers from `common/src/db/query.rs` for filtering and pagination if the package list is large.
- Group the results by license identifier, then for each group call `LicensePolicy::is_compliant()` to set the `compliant` flag.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with JOIN rather than N+1 queries — join `sbom_package`, `package`, and `package_license` in one query.
- Return `Result<LicenseReport, AppError>` following the error handling pattern from `common/src/error.rs`.
- Per constraints doc section 5.2: inspect existing service code before implementing.
- Per constraints doc section 5.4: reuse existing query utilities from `common/src/db/query.rs` rather than writing new query helpers.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service constructor and query pattern with database connection
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package query logic; may be directly reusable for fetching package data
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — standard error type with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a correct `compliant` flag based on the loaded policy
- [ ] Transitive dependencies are included in the report with `transitive: true` when distinguishable
- [ ] The service returns an appropriate error when the SBOM ID does not exist
- [ ] No N+1 query patterns — package and license data fetched in a single JOIN query
- [ ] Code compiles without errors (`cargo build`)

## Test Requirements
- [ ] Unit test: generating a report for an SBOM with packages under MIT (allowed) produces all-compliant groups
- [ ] Unit test: generating a report for an SBOM with packages under GPL-3.0-only (denied) produces non-compliant groups
- [ ] Unit test: generating a report for an SBOM with mixed licenses produces correct compliant/non-compliant counts
- [ ] Unit test: generating a report for a non-existent SBOM returns an error
- [ ] Unit test: verify grouping logic — packages with the same license appear in the same group

## Dependencies
- Depends on: Task 1 — Add license report and policy model structs
- Depends on: Task 2 — Add license policy configuration file and loader

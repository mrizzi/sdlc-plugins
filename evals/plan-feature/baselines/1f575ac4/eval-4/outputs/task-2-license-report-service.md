# Task 2 — Implement license report aggregation service

## Repository
trustify-backend

## Target Branch
main

## Description
Implement a `LicenseReportService` that aggregates package license data from existing database entities, walks transitive dependencies, groups packages by license type, and evaluates compliance against the license policy configuration. This service is the core business logic for the license compliance report feature — it queries existing `package_license` and `sbom_package` data without introducing new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a method to generate a license compliance report for a given SBOM ID

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the report model (if model structs are added here)

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Response model structs: `LicenseReport` (top-level), `LicenseGroup` (per-license grouping with compliance flag), `LicensePackageEntry` (package info within a group)

## API Changes
- Internal service method: `LicenseReportService::generate_report(sbom_id: Id, db: &DatabaseConnection, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` — NEW

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` demonstrates how to query the database using SeaORM, handle errors with `.context()`, and return structured results.
- Query the `sbom_package` entity to get all packages for the given SBOM ID, then join with `package_license` entity to get license information for each package. See `entity/src/sbom_package.rs` and `entity/src/package_license.rs` for the entity definitions.
- For transitive dependency walking: traverse the full dependency tree starting from the SBOM's direct packages through `sbom_package` relationships. If the entity model does not support recursive dependency relationships, flatten all packages linked to the SBOM as the initial implementation.
- Group packages by their license identifier and for each group, use `LicensePolicy::check_compliance()` from Task 1 to determine the `compliant` flag.
- The response shape must match the feature requirement: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use efficient database queries (batch loading, joins) rather than N+1 queries. Reference `common/src/db/query.rs` for shared query builder helpers.
- No new database tables — aggregate exclusively from existing `package_license` and `sbom_package` data.
- Error handling: return `Result<T, AppError>` with `.context()` wrapping, consistent with `modules/fundamental/src/sbom/service/sbom.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Demonstrates the service pattern for database queries, error handling, and result construction.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Shows how to query package entities; may have relevant query patterns for package-license joins.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field definition showing how license data is modeled on the package entity.
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; useful for efficient batch queries.
- `entity/src/package_license.rs` — The Package-License mapping entity that contains the license data to aggregate.
- `entity/src/sbom_package.rs` — The SBOM-Package join table entity needed to find all packages for a given SBOM.

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a `license` field (SPDX identifier), a `packages` array, and a `compliant` boolean
- [ ] Compliance is evaluated using the `LicensePolicy` from Task 1
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM)
- [ ] No new database tables are created — the service uses only existing entities
- [ ] The service returns an appropriate error when the SBOM ID does not exist

## Test Requirements
- [ ] Unit/integration test: generating a report for an SBOM with packages under MIT and Apache-2.0 licenses returns two groups, both marked compliant (assuming default policy allows them)
- [ ] Unit/integration test: generating a report for an SBOM with a GPL-3.0 package returns a group with `compliant: false` (assuming default policy does not allow it)
- [ ] Unit/integration test: generating a report for a non-existent SBOM ID returns an appropriate error
- [ ] Unit/integration test: generating a report for an SBOM with no packages returns an empty groups array

## Dependencies
- Depends on: Task 1 — Add license policy configuration model

# Task 2 — Add license report service with compliance checking

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `LicenseReportService` that generates a license compliance report for a given SBOM. The service queries all packages associated with the SBOM (including transitive dependencies), groups them by license type, and checks each group against the license policy to produce compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with report generation logic
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport and LicenseGroup response structs

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` demonstrates the convention for database queries, error handling with `.context()`, and result types.
- The `LicenseReport` response struct should match the API contract:
  ```
  LicenseReport {
    groups: Vec<LicenseGroup>
  }
  LicenseGroup {
    license: String,
    packages: Vec<PackageLicenseInfo>,
    compliant: bool
  }
  PackageLicenseInfo {
    name: String,
    version: String,
    // additional relevant fields from PackageSummary
  }
  ```
- To resolve transitive dependencies, query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to get license mappings.
- Use SeaORM query patterns from `common/src/db/query.rs` for building the database queries.
- Group packages by their license identifier, then check each group's license against the `LicensePolicy` loaded from configuration (Task 1).
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries.
- All handlers must return `Result<T, AppError>` using the error type from `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service pattern, database query conventions, and error handling approach
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity needed for querying packages by SBOM
- `entity/src/package_license.rs` — Package-License mapping entity needed for resolving license data
- `entity/src/package.rs` — Package entity for package metadata
- `common/src/error.rs::AppError` — standard error type with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReportService` accepts an SBOM ID and returns a `LicenseReport`
- [ ] Report groups all packages (including transitive dependencies) by license type
- [ ] Each group has a `compliant` boolean flag based on the license policy
- [ ] Returns appropriate error when SBOM ID is not found
- [ ] No new database tables are created — aggregates from existing package-license data

## Test Requirements
- [ ] Unit test: service correctly groups packages by license
- [ ] Unit test: service flags non-compliant licenses based on policy
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service returns error for non-existent SBOM ID
- [ ] Unit test: service handles SBOM with no packages (empty report)

## Dependencies
- Depends on: Task 1 — Add license policy configuration model

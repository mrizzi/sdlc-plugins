# Task 3: Implement license report service

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core service logic that generates a license compliance report for a given SBOM. The service queries the database for all packages associated with the SBOM (including transitive dependencies), groups them by license type, evaluates each group against the license policy, and returns a structured `LicenseReport`.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` declaration and integrate LicenseReportService

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for constructor and method signatures.
- The `LicenseReportService` should:
  1. Accept a database connection/pool and a `LicensePolicy` (from Task 2)
  2. Provide a method `generate_report(&self, sbom_id: Uuid) -> Result<LicenseReport, AppError>`
- The report generation logic should:
  1. Verify the SBOM exists using a query pattern similar to `SbomService::fetch` in `modules/fundamental/src/sbom/service/sbom.rs`
  2. Query all packages linked to the SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`)
  3. For each package, retrieve its license(s) from the `package_license` mapping (`entity/src/package_license.rs`)
  4. Walk transitive dependencies by following package relationships in `sbom_package` — packages linked to the SBOM that are dependencies of other packages
  5. Group packages by their license identifier
  6. Evaluate each license group against the `LicensePolicy::is_compliant()` method
  7. Build and return a `LicenseReport` (from Task 1) with computed `totalPackages` and `totalViolations` counts
- Use SeaORM query patterns from `common/src/db/query.rs` for database access.
- Use `AppError` from `common/src/error.rs` for error handling, wrapping database errors with `.context()`.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 individual package lookups. Fetch all `sbom_package` and `package_license` records in two queries, then join in memory.

## Acceptance Criteria
- [ ] `LicenseReportService` is defined with a `generate_report` method
- [ ] Report correctly groups all SBOM packages by license type
- [ ] Transitive dependency licenses are included in the report
- [ ] Each license group has an accurate `compliant` flag based on the loaded policy
- [ ] `totalPackages` and `totalViolations` summary fields are correctly computed
- [ ] Returns `AppError::NotFound` if the SBOM ID does not exist
- [ ] No new database tables are created — uses existing `sbom_package` and `package_license` entities

## Test Requirements
- [ ] Unit test: report correctly groups packages by license (3 MIT packages, 2 Apache-2.0 packages produce 2 groups)
- [ ] Unit test: non-compliant license is flagged with `compliant: false`
- [ ] Unit test: all-compliant SBOM returns `totalViolations: 0`
- [ ] Unit test: SBOM with mixed compliant/non-compliant licenses returns correct violation count
- [ ] Unit test: nonexistent SBOM ID returns a NotFound error

## Dependencies
- Depends on: Task 1 — Define license report data models
- Depends on: Task 2 — Implement license compliance policy configuration

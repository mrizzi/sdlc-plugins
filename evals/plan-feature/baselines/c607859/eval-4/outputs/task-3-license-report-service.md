# Task 3 -- License Report Service

## Repository
trustify-backend

## Description
Implement the `LicenseReportService` that aggregates license data from existing database entities, walks the full transitive dependency tree for an SBOM, groups packages by license type, and evaluates each group against the configured license policy. This service is the core business logic layer for the compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with a method to generate a `LicenseReport` for a given SBOM ID

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (see `SbomService` for the established pattern of database access, error handling, and return types)
- The service method signature should be approximately: `async fn generate_report(&self, sbom_id: &str, db: &impl ConnectionTrait) -> Result<LicenseReport, AppError>`
- Query strategy (use existing entities, no new tables):
  1. Look up the SBOM by ID using existing SBOM entity (`entity/src/sbom.rs`)
  2. Fetch all packages linked to the SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`)
  3. For each package, fetch license mappings via the `package_license` entity (`entity/src/package_license.rs`)
  4. Walk transitive dependencies: follow package relationships through `sbom_package` to include the full dependency tree, not just direct dependencies
  5. Group packages by license identifier
  6. Evaluate each group against `LicensePolicy::is_compliant()`
  7. Build and return the `LicenseReport`
- Use SeaORM query patterns consistent with existing services (see `sbom.rs` for join and relation traversal patterns)
- Use `common/src/db/query.rs` for any shared query helpers if applicable
- Return `AppError` (from `common/src/error.rs`) with `.context()` wrapping for all error paths, matching the existing error handling convention
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batch-loading licenses rather than N+1 queries
- Per constraints doc section 5.2: inspect the actual SeaORM entity definitions and relations before writing queries
- Per constraints doc section 5.4: reuse `PackageService` query patterns from `modules/fundamental/src/package/service/mod.rs` if they overlap

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference pattern for service structure, database access, and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- existing service for querying packages; may contain reusable query logic for fetching packages by SBOM
- `entity/src/package_license.rs` -- existing entity for the package-to-license mapping table
- `entity/src/sbom_package.rs` -- existing join table entity for SBOM-to-package relationships
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- existing error type for consistent error propagation

## Acceptance Criteria
- [ ] Service correctly aggregates all packages for a given SBOM, including transitive dependencies
- [ ] Packages are grouped by license identifier
- [ ] Each group's `compliant` flag is set correctly based on the license policy
- [ ] Overall report `compliant` flag is `false` if any group is non-compliant
- [ ] Missing SBOM returns an appropriate error (not a panic)
- [ ] Performance: report generation completes within 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit/integration test: generate a report for an SBOM with packages under allowed licenses and verify all groups are compliant
- [ ] Unit/integration test: generate a report for an SBOM with packages under denied licenses and verify non-compliant groups are flagged
- [ ] Unit/integration test: verify transitive dependencies are included in the report (not just direct dependencies)
- [ ] Unit/integration test: verify correct grouping when multiple packages share the same license
- [ ] Unit/integration test: requesting a report for a non-existent SBOM returns an error

## Dependencies
- Depends on: Task 1 -- License Policy Configuration Model (for `LicensePolicy` and `is_compliant`)
- Depends on: Task 2 -- License Report Response Models (for `LicenseReport` and `LicenseReportGroup` structs)

# Task 2 -- Add License Report Service

## Repository
trustify-backend

## Description
Implement the license report service that aggregates package-license data from existing
database tables, walks the transitive dependency tree, groups packages by license, and
applies the license policy to flag non-compliant licenses. This service is the core
business logic for the license compliance report feature.

The service must meet the performance requirement of p95 < 500ms for SBOMs with up to
1000 packages. No new database tables are needed -- the service aggregates from existing
`package`, `sbom_package`, and `package_license` entities.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` -- add `license_report` service sub-module if not already declared
- `modules/fundamental/src/sbom/service/mod.rs` -- register the license report service or extend SbomService

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- LicenseReportService implementation

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs`
  (`SbomService`) for structure, error handling, and database access patterns.
- Use SeaORM queries against existing entities:
  - `entity/src/sbom_package.rs` -- to find all packages belonging to an SBOM
  - `entity/src/package_license.rs` -- to resolve license information for each package
  - `entity/src/package.rs` -- for package details
- For transitive dependency walking: query `sbom_package` relationships recursively.
  Consider using a recursive CTE or iterative approach to walk the dependency graph.
  Ensure cycle detection to handle circular dependencies gracefully.
- Load the license policy from the JSON config file using the `LicensePolicy` struct
  from Task 1. Consider accepting the policy path as a configuration parameter.
- Group packages by their license identifier, then check each group against the policy:
  - If `allowed_licenses` is non-empty, a license is compliant only if it appears in the list
  - If a license appears in `denied_licenses`, it is non-compliant regardless of the allowlist
- Return `Result<LicenseReport, AppError>` following the error handling pattern in
  `common/src/error.rs` (use `.context()` wrapping for database errors).
- For performance: consider batch-loading package-license mappings rather than N+1 queries.
  Use a single query with JOINs across `sbom_package` and `package_license` tables.
- Per constraints doc section 5.4: do not duplicate existing functionality -- reuse
  existing query helpers from `common/src/db/query.rs` where applicable.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference implementation
  for service structure, database access patterns, and error handling
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- error type with IntoResponse implementation
- `entity/src/package_license.rs` -- existing Package-License mapping entity to query against
- `entity/src/sbom_package.rs` -- existing SBOM-Package join table for dependency resolution
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- reference for package
  data access patterns

## Acceptance Criteria
- [ ] Service loads license policy from JSON configuration file
- [ ] Service queries all packages (including transitive dependencies) for a given SBOM ID
- [ ] Service groups packages by license identifier
- [ ] Service flags each group as compliant or non-compliant based on the policy
- [ ] Service returns a LicenseReport struct matching the API contract
- [ ] Service handles missing SBOM ID with appropriate AppError (404)
- [ ] Service handles SBOMs with no packages gracefully (returns empty groups)
- [ ] Circular dependencies in the dependency tree do not cause infinite loops

## Test Requirements
- [ ] Unit test: service correctly groups packages by license for a simple SBOM
- [ ] Unit test: service flags denied licenses as non-compliant
- [ ] Unit test: service treats unlisted licenses as non-compliant when allowlist is populated
- [ ] Unit test: service walks transitive dependencies (A depends on B depends on C -- C's license appears in report)
- [ ] Unit test: service handles circular dependencies without panicking
- [ ] Unit test: service returns 404 AppError for non-existent SBOM ID
- [ ] Unit test: service returns empty groups for SBOM with no packages

## Dependencies
- Depends on: Task 1 -- Add License Report Model and Policy Configuration

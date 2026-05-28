# Task 3 — Add license report service with transitive dependency resolution

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the LicenseReportService that generates a license compliance report for a given SBOM. The service aggregates package-license data from existing database tables, walks the full transitive dependency tree via sbom_package relationships, groups packages by license type, and evaluates each group's compliance against the configured license policy. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with a `generate(sbom_id)` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method signatures, error handling, and database interaction patterns.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the codebase convention.
- **Transitive dependency resolution:** Query `entity/src/sbom_package.rs` (SBOM-Package join table) to get all packages associated with the SBOM. Use `entity/src/package_license.rs` (Package-License mapping) to resolve each package's license. Walk the full dependency tree — not just direct dependencies.
- **Grouping logic:** Collect all resolved packages, group them by their license string, and for each group construct a LicenseReportGroup with the compliance flag evaluated via LicensePolicy.
- **Performance requirement:** p95 < 500ms for SBOMs with up to 1000 packages. Use efficient queries — consider a single joined query rather than N+1 queries per package.
- **No new database tables** — aggregate exclusively from existing package-license data in the `package_license` entity.
- Use `common/src/db/query.rs` shared query builder helpers if applicable for constructing the aggregation query.
- Per docs/constraints.md §5.2: Inspect existing code (SbomService, PackageService) before implementing to understand query patterns.
- Per docs/constraints.md §5.4: Reuse existing query helpers and service patterns rather than duplicating.
- Per docs/constraints.md §5.6: Trace the complete data-flow lifecycle (SBOM ID input -> package query -> license resolution -> grouping -> compliance check -> report output) and verify all paths are complete.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service pattern for SBOM operations; follow its structure for database connection handling, error propagation, and method signatures.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Package querying logic that may already handle package-license resolution; check for reusable query methods.
- `common/src/db/query.rs` — Shared query builder helpers for filtering and constructing database queries.
- `entity/src/sbom_package.rs` — SBOM-Package join table entity; use for resolving which packages belong to an SBOM.
- `entity/src/package_license.rs` — Package-License mapping entity; use for resolving each package's license.

## Acceptance Criteria
- [ ] `generate(sbom_id)` returns a LicenseReport with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each group's `compliant` flag correctly reflects the license policy evaluation
- [ ] Non-existent SBOM IDs return an appropriate error
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test: Service correctly groups packages by license
- [ ] Unit test: Transitive dependencies are included in the grouping
- [ ] Unit test: Compliance flags match the configured policy (allowed license -> compliant: true, denied -> compliant: false)
- [ ] Unit test: Empty SBOM (no packages) returns an empty groups list
- [ ] Unit test: SBOM with packages that have no license data handles gracefully

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report response model

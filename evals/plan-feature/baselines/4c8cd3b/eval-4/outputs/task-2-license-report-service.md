## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that generates a license compliance report for a given SBOM. The service aggregates all packages (including transitive dependencies) associated with the SBOM, groups them by license identifier, evaluates each group against the loaded license policy, and returns a structured `LicenseReport`.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a method to generate the compliance report for an SBOM by ID

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- **Service pattern:** Follow the existing service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The service should accept a database connection (from the SeaORM connection pool) and expose a method like `generate_report(db: &DatabaseConnection, sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>`.
- **Data aggregation from existing entities:** Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to get the license for each package. No new database tables are needed — aggregate from the existing entity relationships.
- **Transitive dependency walking:** The SBOM ingestion process (in `modules/ingestor/src/graph/sbom/mod.rs`) stores the full dependency tree via the `sbom_package` join table. Query all `sbom_package` records for the given SBOM ID to capture both direct and transitive dependencies. If the dependency graph requires recursive walking, implement it as an iterative BFS/DFS over the package relationships rather than recursive SQL.
- **Grouping by license:** After collecting all packages with their licenses, group them into `LicenseReportGroup` instances keyed by the SPDX license identifier. Each group contains the list of `PackageSummary` entries and a `compliant: bool` flag.
- **Policy evaluation:** For each license group, look up the license identifier in the `LicensePolicy` rules. Set `compliant = true` if the policy rule is `Allowed`, `compliant = false` if `Denied` or `Review` (or if no rule matches and the default is `Review`).
- **Performance:** The p95 target is < 500ms for SBOMs with up to 1000 packages. Use a single query with JOINs rather than N+1 queries. Use `HashMap<String, Vec<PackageSummary>>` for in-memory grouping.
- **Error handling:** Follow the `Result<T, AppError>` pattern with `.context()` wrapping as used throughout `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing SBOM service demonstrating the service pattern (database connection handling, error wrapping, query structure)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Existing package service for fetching package data; may provide reusable query patterns for package-license joins
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-package join table; use for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — SeaORM entity for package-license mapping; use for resolving license identifiers per package
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse query construction patterns

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each `LicenseReportGroup.compliant` flag correctly reflects the license policy evaluation
- [ ] Packages with licenses not in the policy are flagged as non-compliant (default to `Review`/non-compliant)
- [ ] The service returns an appropriate `AppError` when the SBOM ID does not exist
- [ ] Report generation uses efficient queries (no N+1 patterns)

## Test Requirements
- [ ] Unit test: generate a report for an SBOM with packages under MIT (allowed) and GPL-3.0 (denied) licenses; verify grouping and compliance flags
- [ ] Unit test: generate a report for an SBOM with transitive dependencies and verify all transitive packages appear in the report
- [ ] Unit test: generate a report with a license not in the policy and verify it defaults to non-compliant
- [ ] Unit test: verify that requesting a report for a nonexistent SBOM ID returns an error
- [ ] Unit test: verify performance characteristics — report generation for a mock dataset of 1000 packages completes without N+1 query patterns

## Dependencies
- Depends on: Task 1 — License policy configuration and report models

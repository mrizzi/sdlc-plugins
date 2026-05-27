## Repository
trustify-backend

## Target Branch
main

## Description
Add a license report service that aggregates package-license data from existing database entities, groups packages by license type, walks transitive dependencies via the SBOM package relationships, and flags non-compliant licenses using the license policy configuration. This service provides the core business logic for generating license compliance reports without adding new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods to generate a compliance report for a given SBOM ID
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseGroup and LicenseReport model structs for the report response

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module
- `modules/fundamental/src/sbom/mod.rs` — Ensure the service and model submodules are accessible

## Implementation Notes
- Follow the existing service pattern established by `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`. The license report service should accept a database connection and return structured results.
- Follow the existing model pattern from `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definitions with serde serialization.
- The `LicenseReport` struct should contain: `sbom_id`, `groups: Vec<LicenseGroup>`, `total_packages: usize`, `non_compliant_count: usize`.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- Use existing SeaORM entities for data access: `entity/src/sbom_package.rs` (SBOM-Package join table) and `entity/src/package_license.rs` (Package-License mapping) to query packages and their licenses for a given SBOM.
- To walk transitive dependencies, query `sbom_package` relationships recursively starting from the SBOM's direct packages. Use the existing query helpers in `common/src/db/query.rs` for building efficient queries.
- Load the `LicensePolicy` from `common/src/license_policy.rs` (Task 1) to evaluate compliance for each license group.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider using a single query with JOINs rather than N+1 queries, and batch the license grouping in-memory after fetching.
- Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing SBOM service demonstrating the service pattern, database connection handling, and error wrapping
- `entity/src/package_license.rs` — Package-License entity mapping; reuse for querying license data without creating new tables
- `entity/src/sbom_package.rs` — SBOM-Package join entity; reuse for walking the dependency tree from an SBOM to its packages
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse for building efficient license data queries
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper pattern to follow for structured response types

## Acceptance Criteria
- [ ] A `LicenseReportService` exists that generates a compliance report for a given SBOM ID
- [ ] The report groups all packages by their license type
- [ ] Each license group includes a `compliant` flag evaluated against the license policy
- [ ] Transitive dependencies are included in the report (the full dependency tree is walked)
- [ ] No new database tables are created — all data is aggregated from existing `sbom_package` and `package_license` entities
- [ ] The service returns `Result<LicenseReport, AppError>` following the project error handling pattern
- [ ] The report includes `total_packages` and `non_compliant_count` summary fields

## Test Requirements
- [ ] Unit test: generating a report for an SBOM with packages across multiple license types produces correct grouping
- [ ] Unit test: packages with denied licenses are flagged as non-compliant in their group
- [ ] Unit test: packages with allowed licenses are flagged as compliant in their group
- [ ] Unit test: transitive dependencies are included in the license report (not just direct dependencies)
- [ ] Unit test: generating a report for an SBOM with no packages returns an empty groups list
- [ ] Unit test: `total_packages` and `non_compliant_count` are computed correctly

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader

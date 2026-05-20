# Task 3 — Add LicenseReportService for license aggregation and compliance checking

## Repository
trustify-backend

## Target Branch
main

## Description
Add a LicenseReportService that aggregates package license data from the existing `package_license` entity, walks the transitive dependency tree via `sbom_package` relationships, groups packages by license type, and applies the license policy to flag non-compliant groups. This service is the core business logic for the license compliance report.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService implementation

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report` to expose the new service module

## API Changes
- Internal service API (not HTTP): `LicenseReportService::generate(db: &DatabaseConnection, sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>`

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest)
- The service must:
  1. Query `sbom_package` to get all packages for the given SBOM ID (both direct and transitive)
  2. Join with `package_license` to get the license for each package
  3. Group packages by license identifier
  4. For each group, check the license against the `LicensePolicy` (from Task 1) to determine the `compliant` flag
  5. Return a `LicenseReport` (from Task 2) with all groups
- Use SeaORM query patterns consistent with existing services — see `modules/fundamental/src/sbom/service/sbom.rs` for query builder usage
- Use the shared query helpers from `common/src/db/query.rs` for any filtering or pagination needs
- Mark transitive dependencies: packages linked via intermediate dependency relationships should have `transitive: true` in the PackageLicenseEntry
- Error handling: use `Result<T, AppError>` with `.context()` wrapping per the error handling convention in `common/src/error.rs`
- Performance: the p95 target is < 500ms for SBOMs with up to 1000 packages. Use efficient SQL joins rather than N+1 queries. Consider a single query that joins sbom_package -> package -> package_license
- No new database tables — aggregate exclusively from existing entity data (`entity/src/package.rs`, `entity/src/sbom_package.rs`, `entity/src/package_license.rs`)
- Per constraints (docs/constraints.md) section 5.4: code must not duplicate existing functionality — check SbomService and PackageService for any reusable query logic

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — SbomService demonstrates the service pattern, database connection handling, and error wrapping
- `modules/fundamental/src/package/service/mod.rs` — PackageService fetch/list operations may contain reusable query patterns for package data
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — Package-License mapping entity definition needed for the join query
- `entity/src/sbom_package.rs` — SBOM-Package join table entity needed to find packages belonging to an SBOM

## Acceptance Criteria
- [ ] Service correctly aggregates all packages for a given SBOM ID grouped by license
- [ ] Transitive dependencies are included and correctly marked
- [ ] License policy is applied to determine compliance flags per group
- [ ] Service returns AppError for invalid or non-existent SBOM IDs
- [ ] No new database tables are created — only existing entities are queried
- [ ] Performance: efficient query plan avoids N+1 queries

## Test Requirements
- [ ] Unit test: service returns correct grouping for an SBOM with packages having different licenses
- [ ] Unit test: transitive dependencies are included and marked as `transitive: true`
- [ ] Unit test: compliance flag is `false` for licenses on the denied list
- [ ] Unit test: compliance flag is `true` for licenses on the allowed list
- [ ] Unit test: service returns an error for a non-existent SBOM ID
- [ ] Unit test: licenses not in either allowed or denied list respect the default policy

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report model structs

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package-license data from the existing database, walks the full transitive dependency tree, groups packages by license type, and applies the license policy to determine compliance status for each group. This service uses existing entity data (no new database tables) and produces a LicenseReport ready for serialization by the endpoint.

## Files to Create
- `modules/fundamental/src/license_report/service/mod.rs` — LicenseReportService with the `generate_report` method

## Files to Modify
- `modules/fundamental/src/license_report/mod.rs` — Add `pub mod service;` to register the service sub-module

## Implementation Notes
- Follow the service pattern established by `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) and `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService). Services take a database connection and return domain types.
- The `generate_report` method signature should be: `async fn generate_report(&self, db: &DatabaseConnection, sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>`
- Query the existing `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the given SBOM ID.
- Query the existing `package_license` mapping (`entity/src/package_license.rs`) to get the license for each package.
- Walk transitive dependencies: follow the dependency graph via sbom_package relationships to include indirect dependencies, not just direct ones.
- Group packages by their license string (SPDX identifier). For each group, apply `LicensePolicy::is_compliant()` to set the `compliant` flag.
- Use the existing query helpers from `common/src/db/query.rs` for building database queries.
- All handlers and service methods should return `Result<T, AppError>` using `.context()` wrapping per the existing error handling pattern in `common/src/error.rs`.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use efficient SQL queries with JOINs rather than N+1 queries. Consider a single query that joins sbom_package, package, and package_license.
- Per `docs/constraints.md` §5 (Code Change Rules): Changes must be scoped to the files listed. Code must not duplicate existing functionality — reuse query helpers and entity definitions.
- Per `docs/constraints.md` §2 (Commit Rules): Every commit must reference TC-9004 in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per `docs/constraints.md` §3 (PR Rules): The branch must be named after the Jira issue ID, and PR link must be posted to Jira after opening.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; reuse for constructing the package-license aggregation query
- `entity/src/sbom_package.rs` — Existing SBOM-Package join table entity; use to query packages belonging to an SBOM
- `entity/src/package_license.rs` — Existing Package-License mapping entity; use to retrieve license data for each package
- `entity/src/package.rs` — Package entity for package metadata
- `common/src/error.rs::AppError` — Existing error handling enum; use with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each license group has the correct `compliant` flag based on the provided `LicensePolicy`
- [ ] The service returns an appropriate error when the SBOM ID does not exist
- [ ] No new database tables are created — the service aggregates from existing entity data

## Test Requirements
- [ ] Unit test: Given an SBOM with packages having MIT and GPL-3.0 licenses, the report contains two groups with correct package assignments
- [ ] Unit test: Given a policy that denies GPL-3.0, the GPL-3.0 group is marked `compliant: false` and the MIT group is marked `compliant: true`
- [ ] Unit test: Transitive dependencies are included in the license groups
- [ ] Unit test: Non-existent SBOM ID returns an appropriate error

## Dependencies
- Depends on: Task 1 — License report model and policy (provides LicenseReport, LicenseGroup, and LicensePolicy types)

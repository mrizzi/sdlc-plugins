## Repository
trustify-backend

## Target Branch
main

## Description
Add a license report service method to the SBOM module that aggregates package-license data for a given SBOM, walks transitive dependencies, groups packages by license type, and checks each group against the license policy to produce a compliance report. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- License report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` and wire the service method into SbomService or expose as a standalone function

## Implementation Notes
- Implement a method (e.g., `SbomService::generate_license_report(sbom_id: Id) -> Result<LicenseReport, AppError>`) that:
  1. Fetches all packages associated with the SBOM via the `sbom_package` join table (see `entity/src/sbom_package.rs`)
  2. For each package, retrieves its license(s) from the `package_license` mapping (see `entity/src/package_license.rs`)
  3. Walks transitive dependencies to include the full dependency tree (packages linked through dependency relationships)
  4. Groups packages by license identifier (e.g., "MIT", "Apache-2.0")
  5. Checks each license group against the `LicensePolicy` (from Task 1) to set the `compliant` flag
  6. Returns a `LicenseReport` struct (from Task 2)
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for `SbomService` method structure, database query patterns, and error handling.
- Use SeaORM query patterns consistent with existing code. Reference `common/src/db/query.rs` for shared query builder helpers.
- All error handling must use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batching database queries rather than issuing per-package queries.
- No new database tables are needed -- aggregate from existing `package`, `sbom_package`, and `package_license` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Existing service with fetch/list methods; follow its patterns for database access and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Existing package service; may have query patterns for fetching packages with licenses
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity for retrieving license data
- `common/src/license_policy.rs::LicensePolicy` -- License policy from Task 1 for compliance checking

## Acceptance Criteria
- [ ] Service method returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each license group has a correct `compliant` flag based on the license policy
- [ ] Service returns an appropriate error when the SBOM ID does not exist
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test: generate report for an SBOM with packages under multiple licenses and verify correct grouping
- [ ] Unit test: verify transitive dependencies are included in the report
- [ ] Unit test: verify compliance flags are correctly set based on policy (compliant license -> true, denied license -> false)
- [ ] Unit test: verify error is returned for a nonexistent SBOM ID

## Verification Commands
- `cargo test -p fundamental` -- all tests pass including new license report service tests

## Dependencies
- Depends on: Task 1 -- Add license policy configuration
- Depends on: Task 2 -- Add license report response models

# Task 2: Add license policy configuration and compliance service logic

## Repository

trustify-backend

## Target Branch

main

## Description

Implement the license policy configuration loader and the service method that builds a license compliance report for a given SBOM. The service queries existing package-license data (via the `sbom_package` and `package_license` entities), groups packages by license, evaluates each group against the configured license policy, and returns a `LicenseReport` struct.

The license policy is a JSON configuration file that defines which licenses are approved. Packages with licenses not in the approved list are flagged as non-compliant. The policy also supports a deny-list for explicitly prohibited licenses.

## Files to Create

- `common/src/license_policy.rs` -- Defines `LicensePolicy` struct with `approved_licenses: Vec<String>` and `denied_licenses: Vec<String>` fields. Includes a `load_from_file(path: &Path) -> Result<LicensePolicy>` function and a `is_compliant(&self, license: &str) -> bool` method. Falls back to a sensible default policy if no file is found.
- `modules/fundamental/src/sbom/service/license_report.rs` -- Contains `LicenseReportService` (or an impl block extending `SbomService`) with a method `async fn generate_license_report(&self, sbom_id: Uuid, db: &DbConn, policy: &LicensePolicy) -> Result<LicenseReport, AppError>`. This method queries `sbom_package` joined with `package_license` to collect all packages and their licenses for the given SBOM, then groups by license, checks compliance, walks transitive dependencies, and constructs the `LicenseReport`.

## Files to Modify

- `common/src/lib.rs` -- Add `pub mod license_policy;` to expose the new module.
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to expose the service submodule.

## Implementation Notes

- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs`: accept a `&DbConn` parameter, use SeaORM queries, and return `Result<T, AppError>` with `.context()` error wrapping.
- Use the existing `entity::sbom_package` and `entity::package_license` entities for database queries. No new tables or migrations are needed (per NFR).
- For transitive dependency resolution, walk the SBOM package graph using `sbom_package` relationships. If the dependency tree is flat (no explicit parent-child links in the entity), treat all packages in the SBOM as direct dependencies.
- The license policy file path should be configurable, defaulting to `./license-policy.json` relative to the working directory.
- Target p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with JOINs rather than N+1 queries. Consider collecting all data in one query and grouping in-memory.

## Acceptance Criteria

- [ ] `LicensePolicy` struct loads from a JSON file and provides `is_compliant()` evaluation
- [ ] A default policy is used when no configuration file exists
- [ ] Service method queries package-license data from existing entities without creating new tables
- [ ] Packages are grouped by license in the returned `LicenseReport`
- [ ] Each license group has a `compliant` flag based on the policy evaluation
- [ ] `LicenseReportSummary` fields are correctly computed
- [ ] Transitive dependency licenses are included in the report
- [ ] Error cases return appropriate `AppError` variants

## Test Requirements

- Unit tests for `LicensePolicy::is_compliant()` covering: approved license returns `true`, denied license returns `false`, unknown license returns `false` (default-deny).
- Unit test for `LicensePolicy::load_from_file()` with a valid JSON fixture and with a missing file (falls back to default).
- Service-layer tests are deferred to Task 4 (integration tests) since they require a database connection.

[Description digest: sha256-md:b7c29d4f1e8a036582f9d1ca7b305e6d89af42c10e73b58d64f921a0c8e365f2 would be posted as a comment]

## Repository
trustify-backend

## Description
Implement the license report service logic that aggregates package license data for a given SBOM, walks the transitive dependency tree, groups packages by license, and checks each group against the configured license policy. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` (or a method on the existing `SbomService`) that takes an SBOM ID, queries all packages (including transitive dependencies), groups them by license, evaluates compliance against the policy, and returns a `LicenseReport`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` or extend `SbomService` with the new method

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` methods accept a database connection and return `Result<T, AppError>`. The implementation should:

1. Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM
2. For each package, look up the license via the `package_license` mapping (`entity/src/package_license.rs`)
3. Walk transitive dependencies by following the package relationships in `sbom_package` — this may require a recursive query or iterative graph traversal
4. Group the results by license string using a `HashMap<String, Vec<PackageRef>>`
5. Load the `LicensePolicy` configuration and evaluate each group's compliance
6. Build and return the `LicenseReport` struct

Use the query helpers from `common/src/db/query.rs` for database access patterns. Reference `modules/fundamental/src/package/service/mod.rs::PackageService` for how package queries are structured with SeaORM. For performance (p95 < 500ms for 1000 packages), prefer a single query joining `sbom_package` and `package_license` rather than N+1 queries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct; extend with a `license_report` method or compose with it
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Package query patterns to reuse for fetching package data
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-package relationships
- `entity/src/package_license.rs` — SeaORM entity for package-license mappings
- `common/src/license_policy.rs::LicensePolicy` — Policy evaluation from Task 1

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each license group has a correct `compliant` flag based on the configured policy
- [ ] Packages with no license data are grouped under an "Unknown" license and flagged as non-compliant
- [ ] The service returns an appropriate error if the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: grouping logic correctly groups packages by license
- [ ] Unit test: transitive dependencies are included in the grouping
- [ ] Unit test: compliance flags are correctly set based on policy
- [ ] Unit test: packages with no license are flagged as non-compliant under "Unknown"

## Verification Commands
- `cargo build -p trustify-module-fundamental` — Compiles without errors
- `cargo test -p trustify-module-fundamental -- license_report` — All service unit tests pass

## Dependencies
- Depends on: Task 1 — Define license report response model and license policy config

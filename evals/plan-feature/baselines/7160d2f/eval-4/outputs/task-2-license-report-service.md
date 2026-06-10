## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service logic that aggregates packages by license type, walks transitive dependency trees, and evaluates each license group against the configurable license policy. This service method will be called by the endpoint handler to generate the full compliance report for a given SBOM.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `license_report` module declaration
- `entity/src/package_license.rs` — reference for understanding the existing package-license mapping entity
- `entity/src/sbom_package.rs` — reference for understanding the SBOM-package join table used to walk dependencies

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` with methods to generate the compliance report

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) — services accept a database connection/pool and return `Result<T, AppError>`.
- The service must:
  1. Fetch all packages associated with the given SBOM ID using the `sbom_package` join table
  2. Walk transitive dependencies to include indirect packages (use the existing package relationship data in the `sbom_package` entity)
  3. For each package, look up its license from the `package_license` entity
  4. Group packages by license type
  5. Load the license policy configuration and evaluate each group's compliance
  6. Return a `LicenseReport` with all groups and their compliance flags
- Use SeaORM query patterns consistent with existing services. Reference `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting).
- Error handling: wrap all database operations with `.context()` per the established error handling convention, returning `AppError` variants.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Consider using a single JOIN query to fetch packages with their licenses rather than N+1 queries.
- Per CONVENTIONS.md: follow the existing service module pattern with `Result<T, AppError>` return types and `.context()` error wrapping.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM service with fetch/list patterns to follow for database access
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service with package query patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/db/limiter.rs` — connection pool limiter for managing concurrent queries
- `entity/src/package_license.rs` — existing entity mapping packages to licenses

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a `LicenseReport`
- [ ] Packages are grouped by license type with correct package lists
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] License policy is loaded from a JSON config file
- [ ] Each license group has a correct `compliant` flag based on the policy
- [ ] Returns appropriate error when SBOM ID is not found
- [ ] Meets p95 < 500ms performance target for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: generating a report for an SBOM with packages under MIT and Apache-2.0 licenses groups them correctly
- [ ] Unit test: transitive dependencies are included in the license groups
- [ ] Unit test: a denied license in the policy results in `compliant: false` for that group
- [ ] Unit test: an SBOM with no packages returns an empty report
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- license_report` — all license report service tests pass

## Dependencies
- Depends on: Task 1 — Add license compliance report model structs

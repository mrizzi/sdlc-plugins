## Repository
trustify-backend

## Target Branch
main

## Description
Implement the LicenseReportService that generates license compliance reports for a given SBOM. The service loads the license policy configuration, queries the SBOM's packages and their licenses (including transitive dependencies), groups packages by license type, and evaluates each group against the policy to produce compliance flags. This service is consumed by the endpoint created in Task 3.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods for policy loading, transitive dependency traversal, license aggregation, and compliance evaluation
- `license-policy.json` — default license policy configuration file at the repository root with example allowed/denied license rules

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` declaration
- `modules/fundamental/Cargo.toml` — add any necessary dependencies (if needed for JSON config loading beyond existing serde support)

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for constructor, database access, and error handling conventions.
- The service should accept a database connection and SBOM ID, then:
  1. Load the license policy from the JSON config file (LicensePolicy from Task 1)
  2. Query all packages associated with the SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`)
  3. For each package, resolve its license via the `package_license` mapping (`entity/src/package_license.rs`)
  4. Walk transitive dependencies using the SBOM's dependency graph (inspect the `sbom_package` entity for parent-child relationships)
  5. Group packages by license identifier
  6. Evaluate each group against the policy, setting `compliant: bool`
  7. Return a LicenseReport struct
- Use `Result<T, AppError>` return types with `.context()` wrapping, following the error handling pattern in `common/src/error.rs`.
- Use the query builder helpers from `common/src/db/query.rs` for any database queries.
- Performance: the p95 target is < 500ms for SBOMs with up to 1000 packages. Consider batching database queries rather than issuing per-package queries. Load all packages and licenses in bulk, then perform grouping and evaluation in memory.
- No new database tables should be created — aggregate exclusively from existing `package`, `sbom_package`, and `package_license` entities.
- Per constraints (Section 5, Code Change Rules): reuse existing utilities and shared modules. The query helpers in `common/src/db/query.rs` and the error type in `common/src/error.rs` must be used rather than creating new equivalents.
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern showing database access, query construction, and error handling conventions
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for querying packages and licenses
- `common/src/error.rs::AppError` — standard error type; use for all error returns
- `entity/src/package_license.rs` — existing package-license mapping entity; use for joining packages to their licenses
- `entity/src/sbom_package.rs` — existing SBOM-package join table entity; use for resolving packages within an SBOM
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service; reference for how to query package data

## Acceptance Criteria
- [ ] LicenseReportService generates a LicenseReport from a given SBOM ID
- [ ] Packages are correctly grouped by license identifier
- [ ] Transitive dependency licenses are included in the report
- [ ] Non-compliant licenses are correctly flagged based on the loaded policy
- [ ] The default license-policy.json file is present and parseable
- [ ] The service returns appropriate errors for non-existent SBOM IDs

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service flags non-compliant licenses per a test policy
- [ ] Unit test: service includes transitive dependency licenses in grouping
- [ ] Unit test: service returns error for non-existent SBOM ID
- [ ] Unit test: service handles SBOM with no packages (empty report)
- [ ] Unit test: service handles packages with no license data (unknown/missing license group)

## Verification Commands
- `cargo test --package trustify-module-fundamental license_report` — all license report service tests pass

## Dependencies
- Depends on: Task 1 — Add license report and policy model structs

[sdlc-workflow] Description digest: sha256-md:c09bece33af6f07add57d0cb90895490124cca69e1baa3c890fa8b237143a9c3

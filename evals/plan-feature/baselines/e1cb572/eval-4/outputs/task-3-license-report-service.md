# Task 3 — Add license report service with dependency resolution and compliance evaluation

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core business logic for generating license compliance reports. The service aggregates package-license data from existing database entities, walks transitive dependencies through the SBOM package graph, groups packages by license type, and evaluates each group against the license policy from Task 1. This is the central service layer that the endpoint handler (Task 4) will call.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with `generate_report(sbom_id, policy: &LicensePolicy) -> Result<LicenseReportResponse, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` demonstrates how to query the database using SeaORM entities and return domain model types. Mirror its structure: struct with database connection, constructor, async methods returning `Result<T, AppError>`.
- The service must:
  1. Load the `LicensePolicy` configuration (from the JSON config file created in Task 1)
  2. Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the given SBOM ID
  3. For each package, query `package_license` mapping (`entity/src/package_license.rs`) to get the license
  4. Walk transitive dependencies: use the `sbom_package` relationships to build a dependency tree and include packages at all depths, marking each as direct or transitive
  5. Group packages by license identifier
  6. For each group, evaluate compliance using `LicensePolicy::is_compliant()`
  7. Return a `LicenseReportResponse`
- Use the shared query builder helpers from `common/src/db/query.rs` for database queries, consistent with how `SbomService` and `PackageService` build queries.
- Error handling: wrap all database errors with `.context()` and return `AppError`, following the pattern in `common/src/error.rs`.
- Performance: the NFR requires p95 < 500ms for SBOMs with up to 1000 packages. Batch database queries — load all `sbom_package` and `package_license` records for the SBOM in bulk, then process in memory. Avoid N+1 query patterns.
- No new database tables per NFR — all data comes from existing `package`, `sbom_package`, and `package_license` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Service struct pattern, DB query patterns, and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Package query patterns
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type and `.context()` wrapping pattern
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying package membership and dependency tree
- `entity/src/package_license.rs` — Package-License mapping entity for querying license data

## Acceptance Criteria
- [ ] Service returns a `LicenseReportResponse` with packages grouped by license
- [ ] Each license group has a `compliant` flag based on the loaded license policy
- [ ] Transitive dependencies are included in the report with the `transitive` flag set to true
- [ ] Direct dependencies have the `transitive` flag set to false
- [ ] Report generation completes without N+1 query patterns (bulk loads)
- [ ] Non-existent SBOM IDs return an appropriate `AppError` (not a panic or empty report)

## Test Requirements
- [ ] Unit test: service correctly groups packages by license from mock data
- [ ] Unit test: service marks transitive dependencies correctly (transitive=true vs transitive=false)
- [ ] Unit test: service applies license policy to flag non-compliant groups
- [ ] Unit test: service returns error for non-existent SBOM ID
- [ ] Unit test: service handles SBOM with zero packages (returns empty groups)

## Verification Commands
- `cargo test -p fundamental` — all tests pass including new license report service tests

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license compliance report response model

[sdlc-workflow] Description digest: sha256-md:d03d00093772b3711b84f93e5d454175a3a92b22e924e599abd16692da9c9e50
## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service logic that aggregates package-license data for a given SBOM, walks transitive dependencies, groups packages by license type, and evaluates each group against the configurable license policy. This service powers the license report endpoint and must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add module declaration for the license report service
- `modules/fundamental/src/sbom/service/sbom.rs` — potentially extend `SbomService` with the license report method, or delegate to the new service

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — license report aggregation and generation logic

## Implementation Notes
- The service should query existing package-license data from the `package_license` entity (`entity/src/package_license.rs`) joined with the `sbom_package` entity (`entity/src/sbom_package.rs`) to find all packages belonging to the specified SBOM.
- Walk transitive dependencies: use the SBOM's package relationships (via `sbom_package` join table) to resolve the full dependency tree. The ingestion module in `modules/ingestor/src/graph/sbom/mod.rs` stores these relationships — query the same data to enumerate transitive dependencies.
- Group packages by their license identifier, creating a `LicenseGroup` for each unique license.
- For each group, call `LicensePolicy::is_compliant()` to set the `compliant` flag.
- Follow the query helper patterns from `common/src/db/query.rs` for building database queries with filtering and pagination support.
- Use `common/src/error.rs::AppError` with `.context()` wrapping for all database and service errors.
- Performance consideration: avoid N+1 queries — batch-load all package-license mappings for the SBOM in a single query, then group in-memory. This is critical to meeting the p95 < 500ms requirement for SBOMs with up to 1000 packages.
- No new database tables should be created — this aggregates from existing `package`, `sbom_package`, and `package_license` tables.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the established service pattern for SBOM-related operations
- `modules/fundamental/src/package/service/mod.rs::PackageService` — shows how package data is queried and transformed
- `entity/src/package_license.rs` — the package-license mapping entity to query against
- `entity/src/sbom_package.rs` — the SBOM-package join table for enumerating SBOM packages

## Acceptance Criteria
- [ ] Service aggregates all packages (including transitive dependencies) for a given SBOM ID
- [ ] Packages are correctly grouped by license identifier
- [ ] Each group's `compliant` flag is set based on the configured license policy
- [ ] No new database tables are created — uses existing entity data
- [ ] Returns a well-formed `LicenseReport` struct
- [ ] Returns appropriate error (e.g., 404) when SBOM ID does not exist

## Test Requirements
- [ ] Unit test verifying correct grouping of packages by license
- [ ] Unit test verifying transitive dependency inclusion in the report
- [ ] Unit test verifying compliance flags are correctly set per license policy
- [ ] Unit test verifying error handling for nonexistent SBOM IDs
- [ ] Performance test or benchmark verifying report generation completes within 500ms for 1000 packages

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental -- license_report` — unit tests pass

## Dependencies
- Depends on: Task 1 — Add license compliance report model structs
- Depends on: Task 2 — Add configurable license policy

[sdlc-workflow] Description digest: sha256:65b0cbc200527bb0b808957d2c84f89440e523cd926d547519ef80cd25c3b037

# Task 2 — Add license compliance report service with transitive dependency resolution

## Repository
trustify-backend

## Description
Implement the LicenseReportService that generates a license compliance report for a given SBOM. The service fetches all packages associated with the SBOM (including transitive dependencies by walking the full dependency tree via the sbom_package join table), groups them by license type, evaluates each group against the configured license policy, and returns a LicenseComplianceReport.

## Files to Create
- `modules/fundamental/src/license/service/mod.rs` — LicenseReportService with a `generate_report(db: &DatabaseConnection, sbom_id: Uuid) -> Result<LicenseComplianceReport, AppError>` method

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — Register the service submodule

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` -- the SbomService shows how to accept a database connection and entity ID, query related entities, and return a structured result.
- Use SeaORM to query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the given SBOM ID, then join to `package_license` (`entity/src/package_license.rs`) to retrieve license data for each package.
- For transitive dependency resolution: the SBOM ingestion process (`modules/ingestor/src/graph/sbom/mod.rs`) already parses and stores the full dependency tree in the `sbom_package` table. Query all rows for the given SBOM ID to get both direct and transitive packages.
- Group the resulting packages by their license string, construct a `LicenseGroup` for each unique license, and evaluate compliance using `LicensePolicy::is_compliant()`.
- Use `common/src/db/query.rs` query helpers for database operations where applicable.
- Return `Result<LicenseComplianceReport, AppError>` following the error handling pattern with `.context()` wrapping (see `common/src/error.rs`).
- Per CONVENTIONS.md Key Conventions: all service methods return `Result<T, AppError>` with `.context()` wrapping.
- Performance target from NFRs: p95 < 500ms for SBOMs with up to 1000 packages. Use efficient batch queries (single query with JOIN) rather than N+1 patterns. Avoid loading full package entities if only license data is needed.
- No new database tables -- aggregate exclusively from existing `sbom_package` and `package_license` data per NFR.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service structure, database connection handling, and query patterns
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for package-related database queries
- `entity/src/sbom_package.rs` — existing SBOM-Package join entity for fetching all packages in an SBOM
- `entity/src/package_license.rs` — existing Package-License mapping entity for license lookup
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] LicenseReportService.generate_report(sbom_id) returns a LicenseComplianceReport
- [ ] Report groups all packages by license type (one LicenseGroup per unique license string)
- [ ] Transitive dependency licenses are included (full dependency tree from sbom_package)
- [ ] Each license group has a correct compliant flag based on the configured LicensePolicy
- [ ] Non-existent SBOM ID returns an appropriate AppError (not-found)
- [ ] No new database tables are created (aggregates from existing data per NFR)

## Test Requirements
- [ ] Unit test: service correctly groups packages with different licenses into separate groups
- [ ] Unit test: service marks denied licenses as non-compliant in the report
- [ ] Unit test: service includes transitive dependency packages in the grouping
- [ ] Unit test: service returns AppError for non-existent SBOM ID
- [ ] Unit test: service handles SBOM with no packages (returns empty groups)

## Verification Commands
- `cargo test --package fundamental -- license::service` — all license service tests pass

## Dependencies
- Depends on: Task 1 — Add license policy configuration and model types

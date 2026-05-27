## Repository
trustify-backend

## Target Branch
main

## Description
Add a license report service that aggregates package license data from an SBOM, walks transitive dependencies to collect all licenses, groups packages by license type, and evaluates each group against the license policy to produce a compliance report.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/Cargo.toml` — Add dependency on `common` crate if not already present (for LicensePolicy)

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — use the same database connection handling and error patterns
- The service should:
  1. Load the license policy from the configuration (LicensePolicy from Task 1)
  2. Query the `sbom_package` join table to get all packages for the given SBOM ID
  3. Walk transitive dependencies by following package relationships through `sbom_package` entries
  4. For each package, look up its license from the `package_license` entity
  5. Group packages by license identifier
  6. For each group, evaluate compliance against the loaded LicensePolicy
  7. Return a LicenseReport (from Task 2)
- Use SeaORM query patterns consistent with existing services — see `modules/fundamental/src/sbom/service/sbom.rs` for connection and query conventions
- Query the `package_license` entity (`entity/src/package_license.rs`) to resolve package-to-license mappings
- Use the `sbom_package` entity (`entity/src/sbom_package.rs`) to resolve SBOM-to-package relationships
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages — consider using a single joined query rather than N+1 queries
- No new database tables — aggregate from existing `package`, `sbom_package`, and `package_license` entities
- Return `Result<LicenseReport, AppError>` following the error handling pattern from `common/src/error.rs`
- Per docs/constraints.md §5.4: reuse query patterns from existing services rather than writing new database access patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service pattern, database connection handling, and error wrapping with `.context()`
- `modules/fundamental/src/package/service/mod.rs::PackageService` — shows how to query packages with SeaORM
- `common/src/db/query.rs` — shared query builder helpers that may be useful for filtering and joining
- `entity/src/package_license.rs` — the package-license mapping entity to query
- `entity/src/sbom_package.rs` — the SBOM-package join table entity

## Acceptance Criteria
- [ ] Service correctly aggregates all packages for a given SBOM ID grouped by license
- [ ] Transitive dependencies are included in the license groups
- [ ] Each license group has a correct `compliant` flag based on the license policy
- [ ] Returns appropriate error when SBOM ID does not exist
- [ ] No new database tables are created — uses only existing entities

## Test Requirements
- [ ] Unit test: generate report for SBOM with packages under a single compliant license
- [ ] Unit test: generate report for SBOM with mixed compliant and non-compliant licenses
- [ ] Unit test: verify transitive dependencies are included in the report
- [ ] Unit test: verify error handling for non-existent SBOM ID
- [ ] Unit test: verify performance characteristics — report generation for 1000 packages completes within acceptable bounds

## Dependencies
- Depends on: Task 1 — License policy model
- Depends on: Task 2 — License report model

[sdlc-workflow] Description digest: sha256:7644777b03bb20760be9c6f3240b995127ef2f207ed55492e65625e5adcad4c4

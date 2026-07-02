## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service layer logic for generating a license compliance report for a given SBOM. The service queries all packages associated with the SBOM (including transitive dependencies), groups them by license type using the existing package-license entity data, evaluates each group against the license policy, and returns a populated `LicenseReport`.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` declaration and re-export the service function

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `generate_license_report` function that accepts an SBOM ID and database connection, queries packages and licenses, groups by license, evaluates compliance, and returns `Result<LicenseReport, AppError>`

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for database interaction style (SeaORM queries, connection parameter passing).

The `generate_license_report` function should:
1. Load the `LicensePolicy` from a JSON config file (or a default policy if none exists)
2. Query `sbom_package` join table filtered by the given SBOM ID to get all package IDs
3. Query `package_license` entity to get license mappings for those packages, including transitive dependencies by walking the dependency graph through `sbom_package` relationships
4. Group packages by license string using a `HashMap<String, Vec<PackageSummary>>`
5. For each group, evaluate compliance using `LicensePolicy::is_compliant`
6. Build and return a `LicenseReport` with computed `total_packages` and `non_compliant_count`

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries.

Per CONVENTIONS.md §Error Handling: return `Result<LicenseReport, AppError>` and wrap all database and I/O errors with `.context()` providing descriptive messages. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: place the service logic in the `service/` subdirectory following the existing `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for SeaORM query patterns and database connection handling
- `entity/src/sbom_package.rs` — SeaORM entity for the SBOM-to-package join table
- `entity/src/package_license.rs` — SeaORM entity for package-to-license mappings
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `common/src/error.rs::AppError` — error type with `.context()` support
- `modules/fundamental/src/sbom/model/license_report.rs::LicenseReport` — the response model from Task 1

## Acceptance Criteria
- [ ] `generate_license_report` function queries package-license data for a given SBOM ID
- [ ] Packages are grouped by license type in the report
- [ ] Transitive dependency licenses are included (dependency tree is walked)
- [ ] Each license group has a correct `compliant` flag based on the policy
- [ ] `total_packages` and `non_compliant_count` are correctly computed
- [ ] All database and I/O errors are wrapped with `.context()` and return `AppError`
- [ ] Code compiles without errors (`cargo check -p trustify-fundamental`)

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- Depends on: Task 1 — Define license report models and policy configuration

## Additional Fields
- priority: Major
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira

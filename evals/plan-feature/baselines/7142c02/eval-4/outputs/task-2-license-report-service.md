## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package license data from the database, resolves transitive dependencies, groups packages by license type, and evaluates compliance against a configurable license policy.

This service queries existing package-license data (no new database tables) and builds the `LicenseReport` response struct. It must handle SBOMs with up to 1000 packages within p95 < 500ms.

## Jira Metadata
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods to generate the compliance report, load policy configuration, and resolve transitive dependencies.
- `license-policy.json` — Default license compliance policy configuration file at the repository root.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module.
- `modules/fundamental/Cargo.toml` — Add `serde_json` dependency if not already present for policy file parsing.

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService). The new `LicenseReportService` should:

1. Accept a database connection and SBOM ID as parameters.
2. Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM.
3. For each package, query `package_license` (`entity/src/package_license.rs`) to get license mappings.
4. Walk the dependency tree via `sbom_package` relationships to include transitive dependencies, marking each `LicensePackageRef.transitive` accordingly.
5. Group packages by license string into `LicenseGroup` instances.
6. Load the `LicensePolicy` from the config file and evaluate each group's compliance:
   - License in `allowed_licenses` -> `compliant: true`
   - License in `denied_licenses` -> `compliant: false`
   - Otherwise -> use `default_policy` ("allow" = true, "deny" = false, "review" = false)
7. Build the `LicenseReport` with summary statistics.

Use `common/src/db/query.rs` for any filtering/pagination helpers if the dependency tree query benefits from them. All errors should use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.

For performance, batch-fetch all packages and licenses for the SBOM in two queries rather than N+1 queries per package.

Per CONVENTIONS.md §Module Pattern: follow `model/ + service/ + endpoints/` structure for the license report service layer. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's module file scope.

Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Follow the same service struct pattern, constructor, and database interaction approach
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type for all Result return types
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-to-package relationships
- `entity/src/package_license.rs` — SeaORM entity for package-to-license mappings
- `entity/src/package.rs` — Package entity with name and version fields
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reference for how package queries are structured

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a fully populated `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are resolved and included with `transitive: true`
- [ ] License compliance is evaluated against the loaded `LicensePolicy`
- [ ] Default policy file (`license-policy.json`) is created with sensible defaults (MIT, Apache-2.0, BSD allowed; GPL-3.0, AGPL-3.0 denied)
- [ ] Returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] No new database tables or migrations are introduced
- [ ] Query strategy avoids N+1 patterns (batch fetches packages and licenses)

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service marks transitive dependencies as `transitive: true`
- [ ] Unit test: compliance evaluation correctly flags denied licenses as non-compliant
- [ ] Unit test: compliance evaluation correctly marks allowed licenses as compliant
- [ ] Unit test: default_policy "review" results in `compliant: false` for unlisted licenses
- [ ] Unit test: service returns error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Define license report model structs and compliance policy schema

[sdlc-workflow] Description digest: sha256-md:582e6bd6d42defe9f41ef61905b8d4394ce9fdc10e1c1246b6fe1c338239bf4c

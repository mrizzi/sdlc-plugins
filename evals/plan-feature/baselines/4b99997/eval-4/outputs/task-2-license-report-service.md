## Repository
trustify-backend

## Description
Add `LicenseReport` and `LicenseGroup` model structs and a `generate_license_report` method to `SbomService` that aggregates packages by license, evaluates compliance against the license policy, and walks transitive dependencies to include all package licenses in the report.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport` struct with `groups: Vec<LicenseGroup>`; `LicenseGroup` struct with `license: String`, `packages: Vec<PackageInfo>`, `compliant: bool`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` and re-export types
- `modules/fundamental/src/sbom/service/sbom.rs` — add `generate_license_report(&self, sbom_id: Uuid) -> Result<LicenseReport, AppError>` to `SbomService`

## Implementation Notes
- Follow the model pattern in `modules/fundamental/src/sbom/model/summary.rs` for struct layout and derives.
- The service method queries `entity/src/sbom_package.rs` (join table) to get packages for the SBOM, then `entity/src/package_license.rs` to get license data for each package.
- Group packages by license identifier, then evaluate each group's compliance using `LicensePolicy::is_compliant()` from `common/src/license_policy.rs`.
- Walk transitive dependencies via the package dependency graph to include all transitively-included packages.
- Return 404 via `AppError` if the SBOM ID does not exist.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods as pattern references
- `entity/src/sbom_package.rs` — SBOM-Package join table
- `entity/src/package_license.rs` — Package-License mapping
- `entity/src/package.rs` — package entity with license field
- `common/src/license_policy.rs::LicensePolicy` — policy evaluation (from Task 1)

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs exist with correct fields
- [ ] `generate_license_report` groups packages by license and evaluates compliance
- [ ] Transitive dependencies are included in the report
- [ ] Returns 404 for non-existent SBOM ID

## Test Requirements
- [ ] Unit test: packages are correctly grouped by license
- [ ] Unit test: compliance flags match policy evaluation for each group
- [ ] Unit test: transitive dependencies are included
- [ ] Unit test: 404 for non-existent SBOM

## Dependencies
- Depends on: Task 1 — License policy configuration

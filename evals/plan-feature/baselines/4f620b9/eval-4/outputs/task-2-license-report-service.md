# Task 2 — Add LicenseReportService to aggregate licenses and evaluate compliance

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `LicenseReportService` within the SBOM module that aggregates all packages in an SBOM, groups them by license type, and evaluates each group's compliance against the license policy. This service provides the business logic consumed by the endpoint in Task 3.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — add `license_report` module declaration under the sbom module
- `modules/fundamental/src/sbom/service/mod.rs` — re-export or integrate LicenseReportService
- `modules/fundamental/Cargo.toml` — add dependency on `common` policy module if not already present

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with method `generate_report(sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` that queries packages and their licenses, groups by license, and evaluates compliance
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport` struct containing `groups: Vec<LicenseGroup>` where `LicenseGroup` has fields: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`; and `PackageLicenseEntry` with `name: String`, `version: String`

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` demonstrates how to query data using SeaORM and return structured results.
- Use the `package_license` entity from `entity/src/package_license.rs` to join packages with their licenses. Use the `sbom_package` entity from `entity/src/sbom_package.rs` to scope the query to packages within the target SBOM.
- The query should traverse: `sbom` -> `sbom_package` -> `package` -> `package_license` to collect all licenses for packages in the SBOM, including transitive dependencies.
- Return `Result<LicenseReport, AppError>` consistent with `common/src/error.rs` error handling.
- The model structs should derive `Serialize` for JSON response serialization, following the pattern in `modules/fundamental/src/sbom/model/summary.rs`.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, and include `--trailer="Assisted-by: Claude Code"`.
- Per constraints doc section 5 (Code Change Rules): inspect existing code before modifying; follow patterns in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same service method pattern (accepts database connection, returns Result)
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow the same struct definition and derive pattern for response models
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — the `license` field on this struct confirms that license data is available per-package
- `entity/src/package_license.rs` — the entity mapping between packages and licenses
- `entity/src/sbom_package.rs` — the join entity between SBOMs and packages
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a `compliant` flag evaluated against the provided `LicensePolicy`
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM via `sbom_package`)
- [ ] Packages with no license data are grouped under an "Unknown" license group
- [ ] The service returns `AppError` for invalid SBOM IDs

## Test Requirements
- [ ] Unit test: report correctly groups packages by license type
- [ ] Unit test: compliance flag is `true` for approved licenses and `false` for denied licenses
- [ ] Unit test: packages with unknown licenses are grouped under "Unknown"
- [ ] Unit test: requesting a report for a non-existent SBOM returns an appropriate error

## Dependencies
- Depends on: Task 1 — Add license compliance policy configuration model

[sdlc-workflow] Description digest: sha256-md:34942f756227dc20c1e1a11bb4b936f16428d8b1c3a4edecf00e2f4461d68b87

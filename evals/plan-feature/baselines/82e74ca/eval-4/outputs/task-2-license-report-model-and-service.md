# Task 2 — Implement license report model and service

## Repository
trustify-backend

## Description
Create the license report domain module following the existing module pattern (`model/ + service/ + endpoints/`). This task covers the model structs and the service layer that aggregates license data from existing package-license mappings, walks transitive dependencies, groups packages by license type, and checks each group against the license policy.

## Files to Create
- `modules/fundamental/src/license_report/mod.rs` — module declaration
- `modules/fundamental/src/license_report/model/mod.rs` — model module declaration
- `modules/fundamental/src/license_report/model/report.rs` — `LicenseReport` and `LicenseGroup` response structs
- `modules/fundamental/src/license_report/service/mod.rs` — `LicenseReportService` implementation

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the `license_report` module
- `modules/fundamental/Cargo.toml` — add any new dependencies if needed

## Implementation Notes
- Follow the existing module structure exactly. Reference `modules/fundamental/src/sbom/` as the canonical example — it has `model/`, `service/`, and `endpoints/` subdirectories.
- **Response shape** per the feature requirements:
  ```json
  {
    "groups": [
      {
        "license": "MIT",
        "packages": [{ "name": "...", "version": "..." }],
        "compliant": true
      }
    ]
  }
  ```
- Define `LicenseReport` struct containing `groups: Vec<LicenseGroup>`.
- Define `LicenseGroup` struct with fields: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`.
- Define `PackageRef` struct with fields: `name: String`, `version: String`.
- The `LicenseReportService` must:
  1. Accept an SBOM ID and fetch all packages linked to that SBOM via the `sbom_package` join table (see `entity/src/sbom_package.rs`).
  2. For each package, resolve its license via the `package_license` mapping (see `entity/src/package_license.rs`).
  3. Walk transitive dependencies by following the dependency graph in the SBOM package relationships.
  4. Group all packages (direct and transitive) by their license SPDX identifier.
  5. For each group, check the license against the loaded `LicensePolicy` (from Task 1) to set the `compliant` flag.
- Use SeaORM query patterns consistent with existing services. Reference `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for the query and error-handling patterns.
- Use `common/src/error.rs` `AppError` for error handling with `.context()` wrapping, consistent with the codebase convention.
- No new database tables per the non-functional requirements — aggregate from existing `package`, `sbom_package`, and `package_license` entities.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batch-loading package-license mappings rather than N+1 queries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the established service pattern for fetching and aggregating SBOM-related data via SeaORM
- `modules/fundamental/src/package/service/mod.rs::PackageService` — shows how to query package entities and their relationships
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes the `license` field that this service needs to read
- `entity/src/package_license.rs` — the SeaORM entity for the package-license mapping table
- `entity/src/sbom_package.rs` — the SeaORM entity for the SBOM-package join table
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — the standard error type for all service operations

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageRef` structs are defined with appropriate derives (`Serialize`, `Deserialize`, `Clone`, `Debug`)
- [ ] `LicenseReportService` correctly aggregates packages by license for a given SBOM ID
- [ ] Transitive dependency licenses are included in the report
- [ ] Each license group's `compliant` flag correctly reflects the license policy
- [ ] Service returns an appropriate error (via `AppError`) when the SBOM ID does not exist
- [ ] Query performance uses batch loading to avoid N+1 query patterns

## Test Requirements
- [ ] Unit test: verify packages are correctly grouped by license type
- [ ] Unit test: verify compliance flag is set correctly for allowed, denied, and unknown licenses
- [ ] Unit test: verify transitive dependencies are included in the grouping
- [ ] Unit test: verify error returned for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Add license policy configuration

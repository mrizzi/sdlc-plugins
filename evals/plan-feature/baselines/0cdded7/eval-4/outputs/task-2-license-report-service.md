# Task 2 — Add license report service and response models

## Repository
trustify-backend

## Target Branch
main

## Description
Add the `LicenseReportService` and associated response model structs (`LicenseReport`, `LicenseGroup`) in the fundamental module's sbom domain. The service aggregates package-license data from existing database tables, walks the transitive dependency tree for a given SBOM, groups packages by license type, and flags non-compliant licenses using the license policy configuration from Task 1. No new database tables are required — the service queries the existing `package`, `sbom_package`, and `package_license` entities.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport` and `LicenseGroup` response structs
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with `generate_report(sbom_id, policy) -> Result<LicenseReport, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service
- `modules/fundamental/src/lib.rs` — Ensure sbom module re-exports are updated if needed

## API Changes
- None (this task adds the service layer; the endpoint is added in Task 3)

## Implementation Notes
- **Response model structure:**
  ```
  LicenseReport {
      sbom_id: Uuid,
      generated_at: DateTime<Utc>,
      groups: Vec<LicenseGroup>,
      summary: ReportSummary { total_packages: u32, compliant_count: u32, non_compliant_count: u32 }
  }

  LicenseGroup {
      license: String,          // SPDX identifier
      packages: Vec<PackageRef>,// package name + version
      compliant: bool,          // determined by LicensePolicy
      policy_action: String,    // "allowed", "denied", "review_required"
  }
  ```
- **Transitive dependency resolution:** Query the `sbom_package` join table to get all direct packages for the SBOM, then recursively resolve transitive dependencies through package dependency relationships. Use the existing SeaORM entities in `entity/src/sbom_package.rs` and `entity/src/package.rs`
- **License aggregation:** Join through `entity/src/package_license.rs` to get the license for each package. Group results by license SPDX identifier
- **Policy evaluation:** For each license group, check the license against the `LicensePolicy` from Task 1 to determine the `compliant` flag and `policy_action`
- **Performance:** The requirement specifies p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 patterns. Consider using a single query with JOINs across `sbom_package`, `package`, and `package_license` tables
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` provides the model for how services interact with SeaORM entities and return domain types
- Follow the model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct organization and serde serialization
- Error handling: use `Result<T, AppError>` with `.context()` wrapping, matching the pattern in `common/src/error.rs`

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Follow the service pattern for database queries and entity resolution
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the model serialization pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field that the report aggregates
- `entity/src/package_license.rs` — The existing package-license mapping entity used for data aggregation
- `entity/src/sbom_package.rs` — The SBOM-package join table entity for resolving packages within an SBOM
- `common/src/db/query.rs` — Shared query builder helpers for efficient database queries

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a `compliant` flag derived from the license policy
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Packages with no license data are handled gracefully (grouped under an "Unknown" license)
- [ ] The service does not create or require new database tables

## Test Requirements
- [ ] Unit test: generate report for an SBOM with packages under allowed licenses — all groups marked compliant
- [ ] Unit test: generate report for an SBOM with packages under denied licenses — non-compliant groups flagged
- [ ] Unit test: generate report for an SBOM with transitive dependencies — transitive packages appear in the report
- [ ] Unit test: generate report for an SBOM with packages missing license data — grouped under "Unknown"
- [ ] Unit test: generate report with mixed compliant and non-compliant licenses — summary counts are correct

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader

[sdlc-workflow] Description digest: sha256:6e4d852690464ed41959e3d5a5861b41e83a416e4f8ef4eb489a097ac1f81e89

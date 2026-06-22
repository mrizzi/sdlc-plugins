# Task 2 — Add LicenseReportService for compliance aggregation

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the LicenseReportService that aggregates license data from existing SBOM-package and package-license tables, walks transitive dependencies, groups packages by license type, and applies the license policy to flag non-compliant packages. This service provides the core business logic consumed by the license report endpoint.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods to generate a license compliance report for a given SBOM ID
- `modules/fundamental/src/sbom/model/license_report.rs` — Response model structs: LicenseReport, LicenseGroup, PackageLicenseEntry

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module

## API Changes
- Internal service API (not HTTP): `LicenseReportService::generate(sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` — NEW: generates a compliance report for an SBOM

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the SbomService shows how to structure database queries and error handling
- Response model structs should follow the pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`
- LicenseReport struct:
  ```
  LicenseReport {
    sbom_id: Uuid,
    groups: Vec<LicenseGroup>,
    total_packages: usize,
    compliant_count: usize,
    non_compliant_count: usize,
  }
  ```
- LicenseGroup struct:
  ```
  LicenseGroup {
    license: String,          // SPDX identifier
    packages: Vec<PackageLicenseEntry>,
    compliant: bool,          // based on policy evaluation
    policy_action: String,    // "allowed", "denied", "review"
  }
  ```
- Query existing data by joining: `sbom_package` (to get packages in an SBOM) -> `package` -> `package_license` (to get each package's license)
- For transitive dependency resolution: walk the dependency tree from the SBOM root. The SBOM ingestion graph in `modules/ingestor/src/graph/sbom/mod.rs` shows how packages are linked — follow the same relationship structure for traversal
- Use `common/src/db/query.rs` helpers for building efficient queries
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider:
  - Batch-loading package-license relationships instead of N+1 queries
  - Collecting all package IDs first, then fetching licenses in a single query
- Per docs/constraints.md section 5.4: reuse existing query patterns from `common/src/db/query.rs` rather than writing raw SQL
- Per docs/constraints.md section 5.2: inspect SbomService and PackageService before implementing to understand the existing database access patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service showing database query patterns, error handling, and how to fetch SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for package data access; may provide methods to fetch packages by SBOM
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `entity/src/package_license.rs` — existing SeaORM entity for the package-license mapping; use directly for queries
- `entity/src/sbom_package.rs` — existing SeaORM entity for the SBOM-package join table
- `common/src/error.rs::AppError` — use for all error cases with `.context()` wrapping

## Acceptance Criteria
- [ ] LicenseReportService generates a report grouping all packages in an SBOM by their license type
- [ ] Each license group includes a compliance flag based on the configured license policy
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Packages with no license information are grouped under an "Unknown" license and flagged according to the policy's default action
- [ ] The service handles SBOMs that do not exist by returning an appropriate AppError

## Test Requirements
- [ ] Unit test: generate report for an SBOM with packages having only allowed licenses — all groups marked compliant
- [ ] Unit test: generate report for an SBOM with a mix of allowed and denied licenses — correct compliance flags per group
- [ ] Unit test: generate report including transitive dependencies — verify packages from the full dependency tree appear
- [ ] Unit test: generate report for an SBOM with packages missing license data — grouped as "Unknown" with correct default policy
- [ ] Unit test: generate report for a non-existent SBOM ID — returns appropriate error

## Dependencies
- Depends on: Task 1 — Add license policy configuration model

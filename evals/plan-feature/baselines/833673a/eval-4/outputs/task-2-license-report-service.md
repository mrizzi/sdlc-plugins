## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates all package licenses for a given SBOM, groups them by license type, walks the transitive dependency tree, and checks each group against the license policy to produce a structured compliance report. This service is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/license/service/mod.rs` — LicenseReportService with report generation logic
- `modules/fundamental/src/license/model/report.rs` — LicenseReport, LicenseGroup, and PackageLicenseEntry response structs

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — Register the service submodule
- `modules/fundamental/src/license/model/mod.rs` — Register the report model submodule

## Implementation Notes
The service must:

1. Accept an SBOM ID and fetch all packages linked to that SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`).
2. For each package, retrieve its license data from the `package_license` mapping (`entity/src/package_license.rs`).
3. Walk the full transitive dependency tree — packages may reference other packages as dependencies, so the service must recursively resolve all transitive dependencies and include their licenses.
4. Group packages by license identifier (e.g., all MIT packages in one group, all Apache-2.0 packages in another).
5. For each group, check the license against the `LicensePolicy` (from Task 1) to set a `compliant` flag.
6. Return a `LicenseReport` struct containing the grouped data.

The response structs should be:
- `LicenseReport { groups: Vec<LicenseGroup> }`
- `LicenseGroup { license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`
- `PackageLicenseEntry { name: String, version: String, transitive: bool }`

Follow the service pattern established by `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — the service takes a database connection and returns `Result<T, AppError>`.

Use query helpers from `common/src/db/query.rs` for database access. The report must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages, so avoid N+1 queries — batch-load package licenses in a single query where possible.

No new database tables are needed — aggregate from existing `package`, `sbom_package`, and `package_license` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow this service's structure for constructor, dependency injection, and error handling patterns
- `common/src/db/query.rs` — reuse shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — existing entity for package-to-license mapping, use directly for queries
- `entity/src/sbom_package.rs` — existing entity for SBOM-to-package join, use for fetching packages by SBOM ID
- `common/src/error.rs::AppError` — reuse for all error returns

## Acceptance Criteria
- [ ] `LicenseReportService` generates a report for a given SBOM ID
- [ ] Report groups packages by license identifier
- [ ] Transitive dependencies are included with `transitive: true` flag
- [ ] Each group has a `compliant` flag set based on the license policy
- [ ] Packages with no license data are grouped under an "Unknown" license group
- [ ] Service returns `AppError` for non-existent SBOM IDs
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: report correctly groups packages by license
- [ ] Unit test: transitive dependencies are included and flagged
- [ ] Unit test: compliance flag is set correctly for allowed, denied, and unlisted licenses
- [ ] Unit test: packages with no license are grouped under "Unknown"
- [ ] Unit test: service returns error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — License policy configuration

[sdlc-workflow] Description digest: sha256-md:a1a5dd1ce0ddb58857d35a06bd1ebaaa033e08058151c39795900ddc2a18e310

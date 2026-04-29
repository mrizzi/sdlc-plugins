# Task 2 — Add license report model and service

## Repository
trustify-backend

## Description
Create the license report data model and service layer that aggregates package-license data for a given SBOM, walks transitive dependencies, groups packages by license type, and flags non-compliant licenses using the license policy from Task 1. This service is the core business logic for the license compliance report feature.

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `license_report` module declaration
- `modules/fundamental/Cargo.toml` — add dependency on common (for LicensePolicy) if not already present

## Files to Create
- `modules/fundamental/src/license_report/mod.rs` — module root, re-exports
- `modules/fundamental/src/license_report/model/mod.rs` — LicenseReport and LicenseGroup structs
- `modules/fundamental/src/license_report/service/mod.rs` — LicenseReportService with report generation logic

## API Changes
- None (this task is service-layer only; the endpoint is added in Task 3)

## Implementation Notes
- **Model structs** — Define in `model/mod.rs`:
  - `LicenseGroup` — `{ license: String, packages: Vec<PackageLicenseEntry>, compliant: bool }`
  - `PackageLicenseEntry` — `{ name: String, version: String, purl: Option<String> }` (subset of package info relevant to the report)
  - `LicenseReport` — `{ sbom_id: String, groups: Vec<LicenseGroup>, generated_at: DateTime }` 
  - All structs derive `Serialize` for JSON response serialization
- **Service logic** — Define `LicenseReportService` in `service/mod.rs`:
  1. Accept an SBOM ID and a database connection
  2. Query `sbom_package` join table to get all packages for the SBOM (use existing entity from `entity/src/sbom_package.rs`)
  3. For each package, query `package_license` mapping (from `entity/src/package_license.rs`) to get license identifiers
  4. Walk transitive dependencies — follow package dependency relationships through the `sbom_package` join to include indirect dependencies
  5. Group packages by license identifier
  6. For each group, use `LicensePolicy::is_compliant()` to set the `compliant` flag
  7. Return `LicenseReport`
- **Performance** — The requirement is p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries rather than N+1 per-package lookups. Load all package-license mappings for the SBOM in a single query, then group in memory
- **No new database tables** — aggregate exclusively from existing `sbom_package` and `package_license` entities
- Follow the service pattern established by `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` — accept a database connection, return `Result<T, AppError>`
- Follow the model pattern from `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`

## Reuse Candidates
- `entity/src/package_license.rs` — existing entity for package-license mapping, use for license data queries
- `entity/src/sbom_package.rs` — existing entity for SBOM-package join, use for package enumeration
- `entity/src/package.rs` — existing package entity with fields needed for PackageLicenseEntry
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow this service pattern for structure and error handling
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — includes license field, reference for field naming
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `LicenseReportService` generates a `LicenseReport` grouping all packages by license
- [ ] Transitive dependencies are included in the report
- [ ] Each license group has the correct `compliant` flag based on the configured policy
- [ ] No new database tables are created — only existing entities are queried
- [ ] Batch queries are used to avoid N+1 performance issues

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service correctly flags non-compliant licenses based on policy
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service handles SBOM with no packages (returns empty groups)
- [ ] Unit test: service handles packages with no license data (groups under "Unknown" or similar)

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader

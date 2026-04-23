## Repository
trustify-backend

## Description
Create the license report model structs and the service that generates a license compliance report for a given SBOM. The service aggregates package-license data from existing database entities, walks transitive dependencies through the SBOM-package relationships, groups packages by license, and evaluates each group against the license policy from Task 1 to produce compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- Model structs for the license report response: `LicenseReport` (top-level), `LicenseGroup` (per-license grouping with compliance flag), and `LicensePackageEntry` (package info within a group)
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with a `generate(db: &DatabaseConnection, sbom_id: Uuid) -> Result<LicenseReport, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` declaration
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` declaration

## Implementation Notes
- The `LicenseReport` struct should contain a `groups: Vec<LicenseGroup>` field. Each `LicenseGroup` has: `license: String`, `packages: Vec<LicensePackageEntry>`, and `compliant: bool`.
- `LicensePackageEntry` should contain at minimum `name: String` and `version: String` fields.
- All model structs should derive `Serialize`, `Deserialize`, `Clone`, `Debug` following the pattern in `modules/fundamental/src/sbom/model/summary.rs`.
- The service should query packages linked to the SBOM via the `entity/src/sbom_package.rs` join entity, then resolve each package's license(s) via `entity/src/package_license.rs`.
- For transitive dependencies, walk the SBOM package graph recursively. Use the SBOM-package relationships already stored during ingestion (see `modules/ingestor/src/graph/sbom/mod.rs` for how packages are linked).
- Group the collected packages by their license identifier string.
- For each group, call `LicensePolicy::evaluate()` from Task 1 to determine compliance. A group is `compliant: true` only if the status is `Compliant`. `NonCompliant`, `ReviewRequired`, and `Unknown` statuses all set `compliant: false`.
- Use `common/src/db/query.rs` query builder helpers for database access patterns.
- The report must meet the p95 < 500ms performance requirement for SBOMs with up to 1000 packages. Consider fetching all package-license mappings for the SBOM in a single query rather than N+1 queries.
- No new database tables are needed -- aggregate entirely from existing `sbom_package` and `package_license` entities.

## Reuse Candidates
- `entity/src/sbom_package.rs` -- SBOM-Package join entity for resolving which packages belong to an SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity for resolving license data per package
- `entity/src/package.rs` -- Package entity for package name and version fields
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Reference for service patterns (database connection handling, error wrapping)
- `common/src/db/query.rs` -- Query builder helpers for filtering
- `common/src/error.rs::AppError` -- Error type with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReport` struct serializes to JSON matching the format: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Service correctly groups all packages in an SBOM by license
- [ ] Transitive dependencies are included in the report
- [ ] Each group's `compliant` flag reflects the license policy evaluation
- [ ] Packages with no license data are grouped under an "Unknown" license group marked non-compliant
- [ ] Performance: report generation completes in under 500ms for 1000 packages

## Test Requirements
- [ ] Unit test: grouping logic correctly groups packages by license
- [ ] Unit test: compliance flag is `true` for allowed licenses, `false` for denied/unknown
- [ ] Unit test: packages with no license appear in an "Unknown" group
- [ ] Unit test: empty SBOM (no packages) returns an empty groups array

## Dependencies
- Depends on: Task 1 -- License policy configuration (provides `LicensePolicy` and `ComplianceStatus`)

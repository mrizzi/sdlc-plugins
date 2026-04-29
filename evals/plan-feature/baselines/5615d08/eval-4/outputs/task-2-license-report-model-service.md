## Repository
trustify-backend

## Description
Implement the license report domain model and service layer that aggregates package license data from an SBOM, groups packages by license, walks transitive dependencies, and flags compliance violations using the license policy configuration. This is the core business logic for the license compliance report feature (TC-9004).

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Data model structs: `LicenseReport` (top-level report), `LicenseGroup` (packages grouped by license with a `compliant` flag), and `LicenseReportPackage` (package summary within a group)
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a method to generate the compliance report for a given SBOM ID, querying the database for all packages (including transitive dependencies) linked to the SBOM and grouping them by license

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/Cargo.toml` — Add dependency on `common` crate if not already present (needed for `LicensePolicy`)

## Implementation Notes
- The `LicenseReport` struct should have the shape: `{ sbom_id: String, generated_at: DateTime, groups: Vec<LicenseGroup>, summary: LicenseReportSummary }` where `LicenseReportSummary` contains counts of total packages, compliant packages, and non-compliant packages.
- The `LicenseGroup` struct: `{ license: String, packages: Vec<LicenseReportPackage>, compliant: bool }` — the `compliant` flag is determined by calling `LicensePolicy::is_compliant()` from `common/src/license_policy.rs`.
- The `LicenseReportPackage` struct: `{ name: String, version: String, purl: Option<String> }` — derived from the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs`.
- To walk transitive dependencies, query the `sbom_package` join table from `entity/src/sbom_package.rs` to get all packages linked to the SBOM, then join with `package_license` from `entity/src/package_license.rs` to get license identifiers.
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` — the service takes a database connection and returns `Result<LicenseReport, AppError>`.
- Use the query helpers from `common/src/db/query.rs` for building the database queries.
- All response structs should derive `Serialize` for JSON serialization, following the pattern in existing model files like `modules/fundamental/src/sbom/model/summary.rs`.
- For performance (p95 < 500ms for 1000 packages), execute a single query with JOINs rather than N+1 queries. Group results in application code after fetching.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Reuse the package summary structure as a reference for `LicenseReportPackage` fields
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Follow the same service initialization and query patterns
- `entity/src/sbom_package.rs` — Join table entity for fetching packages belonging to an SBOM
- `entity/src/package_license.rs` — Entity for package-to-license mappings
- `common/src/db/query.rs` — Shared query builder helpers for constructing the aggregation query
- `common/src/license_policy.rs::LicensePolicy` — Policy checker from Task 1

## Acceptance Criteria
- [ ] `LicenseReport` struct correctly represents grouped license data with compliance flags
- [ ] Service queries all packages (including transitive dependencies) linked to an SBOM
- [ ] Packages are grouped by license identifier
- [ ] Each group has a `compliant` flag derived from the license policy
- [ ] Report includes a summary with total, compliant, and non-compliant package counts
- [ ] Service returns `AppError` for non-existent SBOM IDs
- [ ] No new database tables are created — uses existing `sbom_package` and `package_license` data

## Test Requirements
- [ ] Unit test: Grouping logic correctly groups packages by license
- [ ] Unit test: Compliance flag is set correctly based on license policy
- [ ] Unit test: Summary counts match the actual group data
- [ ] Unit test: Empty SBOM (no packages) returns an empty report with zero counts
- [ ] Unit test: SBOM with packages that have no license data handles the edge case gracefully

## Dependencies
- Depends on: Task 1 — License policy configuration (provides `LicensePolicy` struct)

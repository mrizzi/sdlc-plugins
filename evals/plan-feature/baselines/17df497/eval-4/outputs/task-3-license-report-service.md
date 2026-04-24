# Task 3 — Implement license report service with transitive dependency resolution

## Repository
trustify-backend

## Description
Implement the core business logic for generating a license compliance report. The service queries existing package-license data for an SBOM, walks the full transitive dependency tree, groups packages by license identifier, evaluates each group against the configured license policy, and returns a structured `LicenseReport`. This task must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with the report generation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## API Changes
- No new HTTP endpoints in this task (endpoint is Task 4)
- Internal service API: `LicenseReportService::generate(db: &DatabaseConnection, sbom_id: Uuid, policy: &LicensePolicy) -> Result<LicenseReport, AppError>`

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` shows the established pattern for database queries and error handling
- Use SeaORM to query the existing entities:
  - `entity/src/sbom_package.rs` — join table connecting SBOMs to packages; use to find all direct packages for an SBOM
  - `entity/src/package_license.rs` — maps packages to license identifiers; join with packages to get license info
  - `entity/src/package.rs` — package entity with name, version fields
- **Transitive dependency resolution**: walk the dependency tree starting from direct SBOM packages. The `sbom_package` join table should be used to discover direct dependencies; if a separate dependency-edge table exists, use it for transitives. Otherwise, recursively query package relationships. Mark each `PackageRef` with `transitive: true/false` accordingly.
- **Grouping logic**: collect all packages (direct + transitive) with their licenses, group by license identifier using a `HashMap<String, Vec<PackageRef>>`, then evaluate each group against `LicensePolicy::is_compliant()`
- **Performance**: the requirement is p95 < 500ms for up to 1000 packages. Use a single batch query to fetch all packages + licenses for the SBOM rather than N+1 queries. Consider using `find_with_related()` or manual joins.
- **No new database tables**: all data comes from existing `package`, `sbom_package`, and `package_license` entities
- Return `AppError` with appropriate context for missing SBOMs (404) using the pattern from `common/src/error.rs`

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service struct pattern, database connection handling, and query building
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package entities
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error handling with `.context()` wrapping
- `entity/src/sbom_package.rs` — SBOM-to-package join entity
- `entity/src/package_license.rs` — package-to-license mapping entity

## Acceptance Criteria
- [ ] Service returns a complete `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report with `transitive: true` flag
- [ ] Each license group is correctly evaluated against the provided `LicensePolicy`
- [ ] Missing SBOM returns an appropriate 404 error
- [ ] No new database tables or migrations are created
- [ ] Query strategy avoids N+1 patterns (batch loading)

## Test Requirements
- [ ] Unit/integration test: generate a report for an SBOM with known packages and licenses, verify grouping
- [ ] Unit/integration test: verify transitive dependencies appear in the report with correct flag
- [ ] Unit/integration test: verify compliance flags match the policy (allowed licenses = compliant, denied = non-compliant)
- [ ] Unit/integration test: requesting a report for a nonexistent SBOM returns 404 error
- [ ] Unit/integration test: SBOM with no packages returns an empty report (edge case)

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and default policy file
- Depends on: Task 2 — Add license report response model

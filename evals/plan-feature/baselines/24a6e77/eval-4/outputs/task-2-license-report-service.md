# Task 2 — Implement License Report Service

## Repository
trustify-backend

## Description
Implement the `LicenseReportService` that aggregates package-license data from existing database tables, walks the transitive dependency tree for a given SBOM, groups packages by license type, and evaluates each group against the configured license policy to produce a compliance report.

This is the core business logic for the license compliance feature. It must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages, using only existing database tables (no new migrations).

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with the `generate_report` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`): the service takes a database connection (or pool) and provides async methods returning `Result<T, AppError>`.
- **Transitive dependency resolution**: Query `sbom_package` (entity at `entity/src/sbom_package.rs`) to get all packages linked to the SBOM. For each package, query `package_license` (entity at `entity/src/package_license.rs`) to get license mappings. Walk the full dependency tree — not just direct dependencies.
- **Grouping**: Collect all packages into groups keyed by their SPDX license identifier. A package with multiple licenses appears in multiple groups.
- **Policy evaluation**: Load the `LicensePolicy` config (from Task 1). For each group, set `compliant = true` if:
  - The license is in `allowed_licenses` (when allowlist is non-empty), OR
  - The license is NOT in `denied_licenses`
  - If both lists are provided, `denied_licenses` takes precedence.
- **Performance**: Use batch queries rather than N+1 patterns. Consider a single JOIN query across `sbom_package` and `package_license` to fetch all license data for the SBOM in one round trip. The p95 target is < 500ms for 1000 packages.
- Use `common/src/db/query.rs` query builder helpers if applicable for constructing the aggregation query.
- Error handling: wrap all database errors with `.context()` as established in the codebase (see `common/src/error.rs::AppError`).
- Per constraints doc section 5 (Code Change Rules): do not introduce new database tables; aggregate from existing `package_license` and `sbom_package` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same service pattern (constructor, async methods, error handling)
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for querying licenses per package
- `entity/src/package.rs` — Package entity for package metadata
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — standard error type with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (not just direct SBOM packages)
- [ ] Non-compliant licenses are correctly flagged based on the configured policy
- [ ] No new database tables or migrations are introduced
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages (batch query pattern, no N+1)

## Test Requirements
- [ ] Unit test: given a set of packages with known licenses and a policy, verify correct grouping and compliance flags
- [ ] Unit test: verify that a package with multiple licenses appears in multiple groups
- [ ] Unit test: verify denied licenses take precedence over allowed licenses when both lists are configured
- [ ] Unit test: verify empty policy (no allowed/denied lists) marks all licenses as compliant
- [ ] Unit test: verify packages with no license data are handled gracefully (e.g., grouped under "UNKNOWN" or excluded with a warning)

## Dependencies
- Depends on: Task 1 — Add License Report Model and Policy Configuration

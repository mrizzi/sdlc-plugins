# Task 2 — Add license report service with transitive dependency resolution

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that aggregates license data from the existing `package_license` entity, walks the full transitive dependency tree via `sbom_package` relationships, groups packages by license type, and evaluates compliance using the `LicensePolicy` configuration. This is the core business logic for the license compliance report.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — re-export the new `license_report` service module

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id, db, policy)` method

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`): the service takes a database connection and returns `Result<T, AppError>`.
- Use SeaORM queries to join `sbom_package` and `package_license` entities to retrieve all packages and their licenses for a given SBOM ID. Reference the entity definitions in `entity/src/sbom_package.rs` and `entity/src/package_license.rs`.
- For transitive dependency resolution: query all `sbom_package` records for the given SBOM ID. The `sbom_package` join table already links SBOMs to all their packages (including transitive). If the table only stores direct dependencies, implement a recursive walk using package dependency relationships.
- Group the results by license string using a `HashMap<String, Vec<PackageRef>>`.
- For each license group, call `LicensePolicy::check_compliance` to set the `compliant` flag.
- Use the query builder helpers from `common/src/db/query.rs` if applicable for filtering.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries. Consider using `.find_with_related()` or a raw SQL join if SeaORM's query builder does not produce an efficient plan.
- No new database tables — aggregate from existing `package_license` and `sbom_package` data.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same service struct pattern, method signatures, and error handling
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — the Package-License mapping entity to query
- `entity/src/sbom_package.rs` — the SBOM-Package join table entity for resolving packages in an SBOM

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM, not just direct)
- [ ] Each `LicenseGroup` has a `compliant` flag set based on the `LicensePolicy`
- [ ] No new database tables are created
- [ ] The service uses efficient queries (no N+1 query patterns)

## Test Requirements
- [ ] Unit/integration test: generate report for an SBOM with packages having MIT and Apache-2.0 licenses, verify grouping is correct
- [ ] Unit/integration test: generate report with a policy that denies GPL-3.0, verify the GPL group is flagged as non-compliant
- [ ] Unit/integration test: generate report for an SBOM with no packages returns empty groups
- [ ] Unit/integration test: verify transitive dependencies are included in the report

## Dependencies
- Depends on: Task 1 — Add license report response model and policy configuration

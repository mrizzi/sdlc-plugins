# Task 3 — Add license report service logic

## Repository
trustify-backend

## Description
Implement the service layer that generates a license compliance report for a given SBOM. The service aggregates package-license data from existing database entities, walks the full dependency tree (including transitive dependencies), groups packages by license type, and checks each group against the configured license policy to determine compliance. No new database tables are required — the service aggregates from the existing `package_license`, `sbom_package`, and `package` entities.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add module declaration for the license report service
- `modules/fundamental/Cargo.toml` — add dependency on `trustify-common` for `LicensePolicy` if not already present

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` or extend `SbomService` with a `generate_license_report` method

## Implementation Notes
- Follow the existing service pattern. See `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for the established conventions: how services accept database connections, query entities, and return domain models.
- Use the existing SeaORM entities to query package-license data:
  - `entity/src/sbom_package.rs` — join table linking SBOMs to packages
  - `entity/src/package.rs` — package entity
  - `entity/src/package_license.rs` — package-to-license mapping
- For transitive dependency resolution: query all packages linked to the SBOM via `sbom_package`, then recursively resolve their dependencies. If the entity model does not support a recursive dependency graph directly, flatten all packages associated with the SBOM (the ingestion process in `modules/ingestor/src/graph/sbom/mod.rs` already links transitive dependencies during SBOM ingestion).
- Group the resulting packages by their license identifier, then for each group, check compliance using `LicensePolicy::is_compliant()` from `common/src/license_policy.rs` (Task 2).
- Return a `LicenseReport` struct (from Task 1) populated with the grouped data.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single database query with joins rather than N+1 queries. Consider using `.find_with_related()` or manual join queries to fetch all package-license data in one round trip.
- Use `Result<LicenseReport, AppError>` as the return type, following the error handling pattern in `common/src/error.rs`.
- Query builder helpers from `common/src/db/query.rs` may be useful for constructing the aggregation query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM service; follow its patterns for database access and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package service; reference for querying package entities
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting)
- `common/src/license_policy.rs::LicensePolicy` — policy checker from Task 2
- `entity/src/sbom_package.rs` — SBOM-Package join entity for linking SBOMs to their packages
- `entity/src/package_license.rs` — Package-License mapping entity

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a `LicenseReport`
- [ ] All packages linked to the SBOM (including transitive dependencies) are included in the report
- [ ] Packages are grouped by license identifier
- [ ] Each group's `compliant` flag correctly reflects the license policy
- [ ] Returns an appropriate error if the SBOM ID does not exist
- [ ] Uses efficient database queries (no N+1 query patterns)

## Test Requirements
- [ ] Unit/integration test: generate report for an SBOM with packages under multiple licenses — verify correct grouping
- [ ] Unit/integration test: verify that non-compliant licenses are flagged correctly based on policy
- [ ] Unit/integration test: verify that transitive dependencies are included in the report
- [ ] Unit/integration test: verify that requesting a report for a non-existent SBOM returns an error
- [ ] Unit/integration test: verify performance is acceptable for an SBOM with a large number of packages (benchmark or timing assertion)

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass

## Dependencies
- Depends on: Task 1 — Add license compliance report response model
- Depends on: Task 2 — Add license policy configuration

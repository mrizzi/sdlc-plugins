# Task 2 — Implement license report service with transitive dependency resolution

## Repository
trustify-backend

## Description
Implement the license report service that aggregates package-license data from existing database tables, walks the full transitive dependency tree for an SBOM, groups packages by license type, and evaluates each group's compliance against the configured license policy. This service is the core business logic for the license compliance report feature.

The service must operate entirely on existing data — no new database tables are introduced. It reads from the `package`, `sbom_package`, and `package_license` entities to collect all packages and their licenses for a given SBOM, including transitive dependencies.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` (or a method on the existing `SbomService`) implementing: fetch all packages for an SBOM including transitive dependencies, group by license, evaluate compliance against the loaded `LicensePolicy`, and return a `LicenseReport`.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` or extend `SbomService` with the license report method.

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService: fetch, list, ingest`). The license report logic can either be a new method on `SbomService` or a separate `LicenseReportService` — prefer extending `SbomService` if it keeps the module cohesive.
- Use SeaORM queries to fetch data from existing entities: `entity/src/sbom_package.rs` (SBOM-Package join), `entity/src/package.rs` (Package entity), and `entity/src/package_license.rs` (Package-License mapping).
- Transitive dependency resolution: walk the SBOM's package relationships recursively. The `sbom_package` join table links SBOMs to their direct packages; use the package dependency graph (if modeled) to resolve transitive deps. If no explicit dependency graph exists in the entity layer, collect all packages linked to the SBOM via `sbom_package` as the full package set.
- Use shared query helpers from `common/src/db/query.rs` for any filtering or pagination operations.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider:
  - Batch-loading all packages and licenses in a single query rather than N+1 queries
  - Using `IN` clauses or joins to fetch all package-license mappings at once
  - Building the grouping in-memory after a single database roundtrip
- Compliance evaluation: for each license group, check if the license SPDX identifier is in the policy's `denied` list (mark `compliant: false`), `allowed` list (mark `compliant: true`), or apply the `default_policy` action.
- Error handling: return `Result<LicenseReport, AppError>` using `.context()` wrapping per the codebase convention in `common/src/error.rs`.
- Per constraints doc section 5.4, do not duplicate existing query patterns — reuse query builder helpers from `common/src/db/query.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list patterns and database access setup to follow.
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination.
- `entity/src/sbom_package.rs` — SeaORM entity for the SBOM-Package join table.
- `entity/src/package_license.rs` — SeaORM entity for the Package-License mapping.
- `entity/src/package.rs` — SeaORM entity for the Package table.

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a `compliant` flag correctly evaluated against the loaded `LicensePolicy`
- [ ] Transitive dependency licenses are included in the report (not just direct dependencies)
- [ ] Packages with licenses in the policy's `denied` list are flagged as non-compliant (`compliant: false`)
- [ ] Packages with licenses in the policy's `allowed` list are flagged as compliant (`compliant: true`)
- [ ] Packages with licenses not in either list follow the `default_policy` action
- [ ] The service returns an appropriate error when the SBOM ID does not exist
- [ ] No new database tables are created — all data is aggregated from existing entities

## Test Requirements
- [ ] Unit test: service correctly groups packages by license from mock data
- [ ] Unit test: service flags denied licenses as non-compliant
- [ ] Unit test: service flags allowed licenses as compliant
- [ ] Unit test: service applies default policy to licenses not in allowed/denied lists
- [ ] Unit test: service includes transitive dependency packages in the report
- [ ] Unit test: service returns an error for a non-existent SBOM ID
- [ ] Unit test: service handles an SBOM with zero packages (returns empty groups)

## Dependencies
- Depends on: Task 1 — Add license policy configuration and report models

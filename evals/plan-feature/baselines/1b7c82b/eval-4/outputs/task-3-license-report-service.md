## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service layer that generates a license compliance report for a given SBOM. The service queries all packages associated with the SBOM (including transitive dependencies), groups them by license, and applies the license policy to flag non-compliant groups. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id, db, policy) -> Result<LicenseReport, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` declaration and optionally wire into `SbomService`

## Implementation Notes
Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs`. The service method should:

1. **Validate SBOM exists** — Query `entity/src/sbom.rs` by ID. Return `AppError::NotFound` if missing. Follow the pattern in `SbomService::fetch()`.

2. **Query packages for the SBOM** — Use `entity/src/sbom_package.rs` to find all packages linked to the SBOM. Join with `entity/src/package.rs` to get package details.

3. **Resolve transitive dependencies** — Walk the dependency tree through `sbom_package` relationships. The SBOM ingestion in `modules/ingestor/src/graph/sbom/mod.rs` stores dependency relationships during parsing; use the same linkage to traverse the full tree. Implement iterative (not recursive) traversal to avoid stack overflow on deep trees, using a visited set to handle circular dependencies.

4. **Fetch license data** — Join with `entity/src/package_license.rs` to get the license for each package. Packages without a license entry should be grouped under an "Unknown" license bucket and flagged as non-compliant.

5. **Group by license** — Aggregate packages into `LicenseGroup` structs keyed by license identifier (SPDX format).

6. **Apply policy** — Use `LicensePolicy::is_compliant()` from `modules/fundamental/src/sbom/service/license_policy.rs` to set the `compliant` field on each group.

7. **Build response** — Construct and return a `LicenseReport` (from `modules/fundamental/src/sbom/model/license_report.rs`) with all groups, the SBOM ID, generation timestamp, and policy name.

For performance (p95 < 500ms for 1000 packages), use a single query with JOINs rather than N+1 queries. Leverage `common/src/db/query.rs` for query construction helpers.

No new database tables are required — all data is sourced from existing `package`, `sbom_package`, and `package_license` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same method signature pattern and error handling conventions
- `entity/src/sbom_package.rs` — SBOM-Package join table for querying packages by SBOM
- `entity/src/package_license.rs` — Package-License mapping for fetching license data
- `entity/src/package.rs` — Package entity for package name and version
- `common/src/db/query.rs` — query builder helpers for constructing efficient JOIN queries
- `common/src/error.rs::AppError` — error handling with `.context()` wrapping
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how dependency relationships are stored during ingestion

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each license group has its `compliant` field set based on the loaded `LicensePolicy`
- [ ] Packages without a license are grouped under "Unknown" and flagged as non-compliant
- [ ] Circular dependencies in the package graph are handled without infinite loops
- [ ] The service returns `AppError::NotFound` for non-existent SBOM IDs
- [ ] No new database tables are created
- [ ] The module is exported from `modules/fundamental/src/sbom/service/mod.rs`

## Test Requirements
- [ ] Unit test: packages are correctly grouped by license identifier
- [ ] Unit test: transitive dependencies are included in the grouping
- [ ] Unit test: circular dependencies do not cause infinite loops
- [ ] Unit test: packages without licenses are grouped under "Unknown" and marked non-compliant
- [ ] Unit test: policy is correctly applied to each group (compliant and non-compliant licenses)
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Verification Commands
- `cargo check -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental license_report` — service tests should pass

## Dependencies
- Depends on: Task 1 — Add license report model structs
- Depends on: Task 2 — Add license policy configuration

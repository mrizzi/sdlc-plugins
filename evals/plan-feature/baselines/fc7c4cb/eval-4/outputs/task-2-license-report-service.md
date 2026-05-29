## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that aggregates package license data from existing database tables, walks the transitive dependency tree, groups packages by license type, and evaluates each group against the loaded license policy to produce a `LicenseReport`. This service is the core business logic for the license compliance report feature and must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add module declaration for the new license report service
- `modules/fundamental/src/sbom/mod.rs` — ensure service submodule is re-exported if needed

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` with a `generate_report(sbom_id: Id, db: &DbConn, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` method

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for method signatures, database interaction patterns, and error handling with `.context()`.
- Query package-license data by joining `sbom_package` (from `entity/src/sbom_package.rs`) with `package_license` (from `entity/src/package_license.rs`) for the given SBOM ID. Use the SeaORM query patterns from `common/src/db/query.rs`.
- For transitive dependency walking: query `sbom_package` relationships recursively. If the entity model supports parent-child package relationships, traverse them. Otherwise, flatten all packages linked to the SBOM (since SBOM ingestion in `modules/ingestor/src/graph/sbom/mod.rs` already resolves the full dependency tree during ingestion).
- Group packages by their `license` field (from `PackageSummary` / `package_license` entity). For each group, check the license against `LicensePolicy.denied_licenses` to set `compliant: false`, or against `LicensePolicy.allowed_licenses` for allowlist mode.
- Performance: use a single database query to fetch all packages and licenses for the SBOM, then perform grouping and compliance evaluation in memory. Avoid N+1 queries. Consider using `HashMap<String, Vec<PackageLicenseEntry>>` for O(n) grouping.
- No new database tables should be created — aggregate exclusively from existing `sbom_package` and `package_license` data.
- All errors must be wrapped with `AppError` from `common/src/error.rs` and include context about what operation failed.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service structure, database query patterns, and error handling conventions
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for querying package data from the database
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — the package-license mapping entity to query against
- `entity/src/sbom_package.rs` — the SBOM-package join table for finding packages in an SBOM

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages correctly grouped by license
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM, not just direct dependencies)
- [ ] Each `LicenseGroup` has its `compliant` field correctly set based on the policy's denied/allowed license lists
- [ ] The service aggregates from existing tables only — no new database migrations or tables are introduced
- [ ] Error cases (SBOM not found, database errors) return descriptive `AppError` values

## Test Requirements
- [ ] Unit test: `generate_report` correctly groups 3+ packages with different licenses into separate `LicenseGroup` entries
- [ ] Unit test: `generate_report` marks a group as non-compliant when its license appears in the policy's denied list
- [ ] Unit test: `generate_report` marks a group as compliant when its license appears in the policy's allowed list
- [ ] Unit test: `generate_report` returns an appropriate error when the SBOM ID does not exist
- [ ] Unit test: `generate_report` handles an SBOM with zero packages (returns empty groups list)
- [ ] Unit test: `generate_report` includes transitive dependency packages in the grouping

## Dependencies
- Depends on: Task 1 — License report models and policy configuration

[sdlc-workflow] Description digest: sha256:7329ed65638ae233ce711c723a8c2555a90826ce527248ccc57aa6d4a17fbd36

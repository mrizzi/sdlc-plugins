## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service logic that generates a license compliance report for a given SBOM. This service queries all packages associated with an SBOM (including transitive dependencies), groups them by license identifier, evaluates each group against the loaded license policy, and returns a `LicenseComplianceReport`. The implementation must meet the p95 < 500ms performance target for SBOMs with up to 1,000 packages by aggregating from existing database tables without creating new ones.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — Contains `LicenseReportService` (or extends `SbomService`) with the report generation method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` declaration and wire up the service

## Implementation Notes
Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The service method should accept a database connection/transaction and the SBOM ID as parameters.

The core logic flow:
1. Query `sbom_package` join table (entity defined in `entity/src/sbom_package.rs`) to get all packages for the SBOM, including transitive dependencies linked through the package relationship chain.
2. For each package, look up its license via `package_license` mapping (entity in `entity/src/package_license.rs`).
3. Group packages by license identifier using a `HashMap<String, Vec<PackageLicenseEntry>>`.
4. Load the `LicensePolicy` (from Task 1) and evaluate each license group's compliance.
5. Construct and return `LicenseComplianceReport` with computed `non_compliant_count`.

For transitive dependency walking: query all packages linked to the SBOM through `sbom_package`, which should already include transitive dependencies stored during ingestion (see `modules/ingestor/src/graph/sbom/mod.rs` for how packages are linked during SBOM ingestion).

Use SeaORM query patterns from `common/src/db/query.rs` for filtering. All errors should be wrapped with `.context()` and return `Result<LicenseComplianceReport, AppError>` per the error handling pattern in `common/src/error.rs`.

For performance: use a single query with JOINs across `sbom_package` and `package_license` rather than N+1 queries. Consider using `.find_also_related()` or a custom select to fetch packages with their licenses in one round-trip.

Per CONVENTIONS.md (Key Conventions from repository structure): all handlers/services return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md (Key Conventions from repository structure): use shared query builder helpers for filtering, pagination, sorting.
Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with database query patterns for SBOM-related data; reuse connection handling and query structure
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type with `IntoResponse` implementation; use for all error returns
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-package relationships; use to query packages for an SBOM
- `entity/src/package_license.rs` — SeaORM entity for package-license mappings; use to resolve licenses per package

## Acceptance Criteria
- [ ] Service method accepts SBOM ID and returns `LicenseComplianceReport`
- [ ] Packages are grouped by license identifier with correct package listings
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each license group has a `compliant` flag based on the loaded license policy
- [ ] `non_compliant_count` accurately reflects the number of packages with non-compliant licenses
- [ ] Non-existent SBOM ID returns an appropriate error (not a panic)
- [ ] Report generation completes within 500ms for 1,000 packages (single JOIN query, no N+1)

## Test Requirements
- [ ] Unit test: service correctly groups packages by license from mock data
- [ ] Unit test: service flags non-compliant licenses according to policy
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service returns error for non-existent SBOM ID
- [ ] Unit test: `non_compliant_count` matches the actual number of non-compliant packages

## Dependencies
- Depends on: Task 1 — Add license compliance report models and policy configuration

## additional_fields
- labels: ai-generated-jira
- priority: Major
- fixVersions: RHTPA 1.5.0

## Repository
trustify-backend

## Description
Implement the LicenseReportService that aggregates package-license data from existing database entities, walks transitive dependencies, and evaluates each license against the configured license policy. This service is the core business logic for the license compliance report feature, sitting between the API endpoint and the data layer.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with a method `generate_report(sbom_id: Uuid, db: &DatabaseConnection) -> Result<LicenseReport, AppError>` that queries package-license data for the given SBOM, walks the transitive dependency tree, groups packages by license, evaluates compliance using LicensePolicy, and returns a LicenseReport

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the existing service pattern from `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for structure: methods take a database connection reference, return `Result<T, AppError>`, and use `.context()` for error wrapping
- Use SeaORM queries against the existing `entity/src/sbom_package.rs` join table to find all packages belonging to the SBOM, then use `entity/src/package_license.rs` to retrieve licenses for each package
- For transitive dependency walking: query `sbom_package` to get direct packages for the SBOM, then recursively resolve dependencies through package relationships. If no explicit dependency graph is available in the entity layer, traverse all packages linked to the SBOM (they represent the full resolved dependency set from ingestion per `modules/ingestor/src/graph/sbom/mod.rs`)
- Group the resulting packages by license identifier, creating one LicenseReportGroup per distinct license
- For each group, call `LicensePolicy::is_compliant()` from `common/src/model/license_policy.rs` to set the `compliant` flag
- Load the LicensePolicy once at service construction or application startup, not per-request. Use `std::fs::read_to_string` to read the `license-policy.json` config file and `serde_json::from_str` to deserialize it
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with JOINs rather than N+1 queries. Consider using `sea_orm::QuerySelect` with `.find_with_related()` or manual `JoinType::LeftJoin` to fetch packages and licenses in one query
- Error handling: return `AppError` with appropriate context messages using the pattern from `common/src/error.rs`
- Per constraints doc section 5.4: do not duplicate existing functionality — reuse the existing entity definitions and query patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the established service pattern (method signatures, error handling, DB interaction)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — demonstrates how to query package-related entities
- `entity/src/sbom_package.rs` — existing SBOM-to-package join entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — existing package-to-license mapping entity for retrieving license data
- `common/src/db/query.rs` — shared query builder helpers that may be useful for constructing the aggregation query
- `common/src/error.rs::AppError` — reuse for error handling with `.context()` wrapping

## Acceptance Criteria
- [ ] LicenseReportService.generate_report() returns a LicenseReport with packages correctly grouped by license
- [ ] Each LicenseReportGroup has an accurate `compliant` flag based on the configured LicensePolicy
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM through the dependency tree)
- [ ] The service reuses existing entity definitions (sbom_package, package_license) — no new database tables or migrations
- [ ] Error cases return appropriate AppError variants with descriptive context messages
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages (no N+1 query patterns)

## Test Requirements
- [ ] Unit test: generate_report returns correct groupings for an SBOM with packages having distinct licenses
- [ ] Unit test: generate_report correctly flags non-compliant licenses based on the policy
- [ ] Unit test: generate_report includes transitive dependency packages in the report
- [ ] Unit test: generate_report returns an empty groups list for an SBOM with no packages
- [ ] Unit test: generate_report returns an error for a non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — License policy configuration and report models

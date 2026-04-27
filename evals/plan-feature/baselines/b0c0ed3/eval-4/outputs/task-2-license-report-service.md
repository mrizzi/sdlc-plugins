## Repository
trustify-backend

## Description
Implement the `LicenseReportService` that aggregates package license data for a given SBOM, walks the full dependency tree (including transitive dependencies), groups packages by license type, and evaluates compliance against a configured license policy. This is the core business logic for the license compliance report feature.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — register the new license report service module

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` with methods for report generation

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) — the service struct takes a database connection pool and exposes async methods returning `Result<T, AppError>`.
- The primary method should be `async fn generate_report(&self, sbom_id: Uuid, policy: &LicensePolicyConfig) -> Result<LicenseReport, AppError>`.
- To walk the dependency tree including transitive dependencies:
  1. Query `sbom_package` (entity in `entity/src/sbom_package.rs`) to get all packages linked to the SBOM.
  2. For each package, query `package_license` (entity in `entity/src/package_license.rs`) to get its license information.
  3. The dependency tree walk must be recursive or iterative to capture transitive dependencies — packages that are dependencies of direct dependencies.
- Group the collected packages by their `license` field to build `Vec<LicenseGroup>`.
- For each group, evaluate compliance: `compliant = true` if the license is in `policy.allowed_licenses` or not in `policy.denied_licenses` (depending on policy mode — allowlist vs denylist).
- Use the query builder helpers from `common/src/db/query.rs` for constructing database queries.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider batching database queries rather than issuing N+1 queries per package. Load all `sbom_package` rows for the SBOM in a single query, then load all associated `package_license` rows in a second query, and join in memory.
- No new database tables are needed — aggregate from existing `package`, `sbom_package`, and `package_license` entities.
- Per docs/constraints.md 5.4: reuse existing query helpers and entity definitions rather than duplicating them.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow its structure for service initialization, database connection handling, and error propagation patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for constructing the package aggregation queries
- `entity/src/sbom_package.rs` — SeaORM entity for the SBOM-Package join table; use to query packages belonging to an SBOM
- `entity/src/package_license.rs` — SeaORM entity for the Package-License mapping; use to retrieve license data for each package
- `entity/src/package.rs` — SeaORM entity for the Package table; use to resolve package details
- `common/src/error.rs::AppError` — use for all error handling with `.context()` wrapping

## Acceptance Criteria
- [ ] `LicenseReportService` is implemented with a `generate_report` method
- [ ] Report correctly groups all packages by license type
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Compliance flags are set correctly based on the provided `LicensePolicyConfig`
- [ ] Packages with licenses in `denied_licenses` are flagged `compliant: false`
- [ ] Packages with licenses in `allowed_licenses` are flagged `compliant: true`
- [ ] No new database tables or migrations are created
- [ ] Service is registered in `modules/fundamental/src/sbom/service/mod.rs`

## Test Requirements
- [ ] Unit test: generating a report for an SBOM with all-compliant licenses returns all groups with `compliant: true`
- [ ] Unit test: generating a report for an SBOM with a denied license returns the violating group with `compliant: false`
- [ ] Unit test: transitive dependencies are included in the correct license groups
- [ ] Unit test: empty SBOM (no packages) returns an empty `groups` vector
- [ ] Unit test: multiple packages with the same license are grouped together

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental -- license_report` — expected: all license report service tests pass

## Dependencies
- Depends on: Task 1 — License report model and policy configuration

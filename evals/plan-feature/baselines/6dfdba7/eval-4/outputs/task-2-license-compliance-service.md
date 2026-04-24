## Repository
trustify-backend

## Description
Implement the license compliance report service that aggregates package-license data for a given SBOM, walks the full transitive dependency tree, groups packages by license, and evaluates each group against the configurable license policy. This is the core business logic for the license compliance feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods to generate the compliance report from SBOM data.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module.

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` struct holds a database connection pool and provides async methods that return `Result<T, AppError>`.
- The `LicenseReportService` should provide a primary method `generate_report(db: &DatabaseConnection, sbom_id: &str, policy: &LicensePolicyConfig) -> Result<LicenseReport, AppError>`.
- **Dependency traversal**: Query `entity/src/sbom_package.rs` to get all packages associated with the SBOM. For transitive dependencies, recursively follow package relationships through the `sbom_package` join table. Mark each `PackageLicenseEntry` with `transitive: true/false` based on whether it is a direct or transitive dependency.
- **License aggregation**: For each package, look up its license via `entity/src/package_license.rs`. Group packages by their SPDX license identifier.
- **Policy evaluation**: For each license group, check the `LicensePolicyConfig`:
  1. If the license is in `denied`, set `compliant: false`.
  2. Else if the license is in `allowed`, set `compliant: true`.
  3. Else apply `default_policy` — `"deny"` means `compliant: false`, `"allow"` means `compliant: true`.
- **Performance target**: p95 < 500ms for SBOMs with up to 1000 packages. Use a single batch query to load all SBOM packages and their licenses rather than N+1 individual queries. Use `common/src/db/query.rs` query helpers for efficient database access.
- Load the policy config from the `license-policy.json` file on disk, or accept it as a parameter so the endpoint can optionally support per-request policy overrides in the future.
- Wrap all database errors with `.context()` using `anyhow` or the project's error pattern, consistent with `common/src/error.rs::AppError`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Pattern reference for service struct with database connection and async query methods
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; use for efficient batch queries
- `common/src/error.rs::AppError` — Standard error type; all service methods should return `Result<T, AppError>`
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-Package join; use to query packages belonging to an SBOM
- `entity/src/package_license.rs` — SeaORM entity for Package-License mapping; use to look up each package's license
- `modules/fundamental/src/sbom/model/license_report.rs::LicenseReport` — Output model from Task 1

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` correctly groups packages by license
- [ ] Transitive dependencies are included and marked with `transitive: true`
- [ ] Policy evaluation correctly classifies licenses as compliant or non-compliant based on `allowed`, `denied`, and `default_policy`
- [ ] `non_compliant_count` on the report accurately reflects the number of non-compliant license groups
- [ ] No N+1 query patterns — packages and licenses are loaded in batch queries
- [ ] All errors are wrapped with `.context()` and return `AppError`
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Unit test: Given a set of packages with MIT and GPL-3.0-only licenses and a policy that denies GPL-3.0-only, the report correctly flags the GPL group as non-compliant
- [ ] Unit test: Given a policy with `default_policy: "deny"` and an unlisted license (e.g., "Unlicense"), the group is flagged as non-compliant
- [ ] Unit test: Given a policy with `default_policy: "allow"` and an unlisted license, the group is flagged as compliant
- [ ] Unit test: Transitive dependencies are correctly included and marked in the report output
- [ ] Unit test: Empty SBOM (no packages) returns a valid report with empty groups

## Dependencies
- Depends on: Task 1 — Define license policy config and report models

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package-license data for a given SBOM, walks transitive dependencies, groups packages by license, and evaluates compliance against the configured license policy. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with methods for generating the compliance report

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method signatures, database connection handling, and error propagation with `.context()`.
- The service must query `sbom_package` (entity at `entity/src/sbom_package.rs`) to get all packages for a given SBOM ID, then join with `package_license` (entity at `entity/src/package_license.rs`) to retrieve license mappings.
- Use SeaORM query patterns consistent with the existing codebase. Reference `common/src/db/query.rs` for shared query builder helpers if applicable.
- Implement transitive dependency traversal: walk the full dependency tree from the SBOM root, not just direct dependencies. The `sbom_package` join table should contain the relationship graph.
- Group results by license string, creating one `LicenseGroup` per distinct license.
- Load the `LicensePolicy` from `license-policy.json` at service initialization or per-request (prefer loading once and caching). Evaluate each license group's `compliant` flag based on the policy: `true` if the license is in `approved_licenses` or not in `denied_licenses` when `default_policy` is "allow"; `false` if the license is in `denied_licenses` or not in `approved_licenses` when `default_policy` is "deny".
- All errors should return `AppError` from `common/src/error.rs` with appropriate context messages.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Pattern for service struct, database connection handling, and error propagation
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type with `.context()` wrapping pattern
- `entity/src/sbom_package.rs` — SBOM-Package join entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for retrieving license data

## Acceptance Criteria
- [ ] Service method accepts an SBOM ID and returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each `LicenseGroup` has a `compliant` flag evaluated against the license policy
- [ ] License policy is loaded from `license-policy.json` configuration file
- [ ] Errors return `AppError` with descriptive context messages
- [ ] No N+1 query patterns; aggregation uses efficient joined queries

## Test Requirements
- [ ] Unit test: service correctly groups packages by license from mock data
- [ ] Unit test: compliance flag is `true` for approved licenses and `false` for denied licenses
- [ ] Unit test: `default_policy: "deny"` marks unlisted licenses as non-compliant
- [ ] Unit test: `default_policy: "allow"` marks unlisted licenses as compliant
- [ ] Unit test: transitive dependencies are included in the report output
- [ ] Unit test: service returns appropriate error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Define license report model structs and policy configuration

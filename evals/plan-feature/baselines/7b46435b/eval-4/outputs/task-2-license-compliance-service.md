## Repository
trustify-backend

## Target Branch
main

## Description
Add the `license_compliance_report` method to `SbomService` that generates a license compliance report for a given SBOM. The method queries the `sbom_package` join table to find all packages associated with the SBOM, joins with `package_license` to retrieve license information, walks transitive dependencies to include indirect packages, groups results by license, and applies the license policy to determine compliance flags for each group.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `license_compliance_report(&self, sbom_id: Uuid, policy_path: Option<&Path>) -> Result<LicenseComplianceReport, AppError>` method that: (1) verifies the SBOM exists (return 404 error if not), (2) queries `sbom_package` joined with `package` and `package_license` to get all packages and their licenses, (3) walks transitive dependencies by following package dependency relationships, (4) loads the license policy from `policy_path` (or default config), (5) groups packages by license name, (6) sets `compliant` flag per group based on policy

## Implementation Notes
The service method belongs in `modules/fundamental/src/sbom/service/sbom.rs` alongside existing `SbomService` methods (fetch, list, ingest). Use the same `Result<T, AppError>` error handling pattern with `.context()` wrapping from `common/src/error.rs`.

The query strategy should be:
1. First verify the SBOM exists using the same pattern as `SbomService::fetch`
2. Query `sbom_package` (from `entity/src/sbom_package.rs`) joined with `package` (`entity/src/package.rs`) to get all direct packages for the SBOM
3. For each package, join with `package_license` (`entity/src/package_license.rs`) to get the license mapping
4. For transitive dependencies, recursively or iteratively follow package dependency edges. Mark packages as `transitive: true` when they are not direct dependencies of the SBOM
5. Group all `PackageLicenseEntry` items by license string
6. For each group, check the loaded `LicensePolicy` to set the `compliant` flag

Use SeaORM's `find_with_related()` or `select_also()` to perform the joins efficiently. Avoid N+1 queries by loading all package-license mappings in a single query where possible.

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use batch queries and avoid per-package round trips to the database.

Per CONVENTIONS.md: all handlers and service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch/list/ingest methods; follow the same method signature and error handling patterns
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for the initial package lookup
- `entity/src/package.rs` -- Package entity containing package name and version
- `entity/src/package_license.rs` -- Package-License mapping entity containing the license field
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination; reuse for efficient query construction
- `common/src/error.rs::AppError` -- standard error type used across all service methods

## Acceptance Criteria
- [ ] `SbomService::license_compliance_report` method exists and compiles
- [ ] Method returns a `LicenseComplianceReport` with packages grouped by license
- [ ] Each group has a `compliant` flag based on the loaded license policy
- [ ] Transitive dependencies are included and marked with `transitive: true`
- [ ] Returns 404 error for non-existent SBOM IDs
- [ ] No new database tables are created -- aggregation uses existing package-license data

## Test Requirements
- [ ] Unit test: report correctly groups packages by license name
- [ ] Unit test: non-compliant licenses (in denied list) produce `compliant: false` groups
- [ ] Unit test: transitive dependencies are included and correctly marked
- [ ] Unit test: returns error for non-existent SBOM ID
- [ ] Unit test: handles SBOMs with no packages (returns empty groups)

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental license_compliance` -- unit tests pass

## Dependencies
- Depends on: Task 1 -- Create license compliance report model and policy configuration

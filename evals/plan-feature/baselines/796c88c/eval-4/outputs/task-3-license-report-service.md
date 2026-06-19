## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that generates a compliance report for a given SBOM. The service queries the database for all packages associated with the SBOM (including transitive dependencies), groups them by license, evaluates each group against the license policy, and returns a structured `LicenseReport`. This is the core business logic for the license compliance feature.

## Files to Modify
- `modules/fundamental/sbom/service/mod.rs` -- Add `license_report` module declaration

## Files to Create
- `modules/fundamental/sbom/service/license_report.rs` -- `LicenseReportService` with method `generate_report(sbom_id: Uuid, db: &DatabaseConnection, policy: &LicensePolicy) -> Result<LicenseReport, AppError>` that:
  1. Validates the SBOM exists (return 404 if not)
  2. Queries all packages linked to the SBOM via `sbom_package` join table
  3. For each package, fetches license data from `package_license` table
  4. Walks transitive dependencies through the package relationship graph
  5. Groups packages by license identifier
  6. Evaluates each group against the `LicensePolicy`
  7. Constructs and returns a `LicenseReport`

## API Changes
- None (internal service; endpoint is in Task 4)

## Implementation Notes
- Follow the pattern in `modules/fundamental/sbom/service/sbom.rs` for service method signatures and error handling
- Use SeaORM query builder for database access, consistent with existing services
- For transitive dependency traversal, use a single SQL query with recursive CTE or a join-based approach rather than N+1 queries, to meet the p95 < 500ms performance target
- Handle packages with no license data by grouping them under an "UNKNOWN" license category
- Handle packages with multiple licenses (e.g., dual-licensed "MIT OR Apache-2.0") by including the package in each applicable license group
- Use `common/src/error.rs` `AppError` for error handling with `.context()` wrapping
- The service should accept `&LicensePolicy` as a parameter so the endpoint layer handles loading the policy (dependency injection pattern)
- Consider using `HashMap<String, Vec<LicensePackageRef>>` as an intermediate grouping structure before converting to `Vec<LicenseGroup>`

## Acceptance Criteria
- [ ] Service correctly groups packages by license for a given SBOM
- [ ] Transitive dependencies are included in the report with `is_transitive: true`
- [ ] Each license group has a correct compliance flag based on the license policy
- [ ] Packages with no license are grouped under "UNKNOWN"
- [ ] Packages with multiple licenses appear in all applicable groups
- [ ] Returns `AppError::NotFound` if the SBOM ID does not exist
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages
- [ ] Summary counts (total, compliant, non-compliant, unknown) are accurate

## Test Requirements
- [ ] Unit test: group packages by license correctly
- [ ] Unit test: transitive dependencies are marked with `is_transitive: true`
- [ ] Unit test: packages with no license are grouped under "UNKNOWN"
- [ ] Unit test: dual-licensed packages appear in multiple groups
- [ ] Unit test: compliance flags match the policy evaluation
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Dependencies
- Depends on: Task 1 -- Define license policy configuration model
- Depends on: Task 2 -- Define license report response models

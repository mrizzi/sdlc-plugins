## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that aggregates package-license data for a given SBOM, walks transitive dependencies, groups packages by license, and evaluates each group against the license policy. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — Implement a `LicenseReportService` (or add a `license_report` method to the existing `SbomService`) with the following logic:
  1. Given an SBOM ID, query the `sbom_package` join table to get all packages associated with the SBOM
  2. For each package, look up the license via the `package_license` entity
  3. Walk transitive dependencies by following package dependency relationships in the SBOM package graph
  4. Group all packages (direct and transitive) by their license identifier
  5. For each license group, evaluate compliance using `LicensePolicy::evaluate`
  6. Build and return a `LicenseReport` with all groups and the computed summary

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` declaration and register the service

## Implementation Notes
- Use SeaORM query patterns consistent with existing services like `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`
- Query the `package_license` entity from `entity/src/package_license.rs` to get license mappings
- Use `sbom_package` entity from `entity/src/sbom_package.rs` to find packages belonging to the SBOM
- For transitive dependency walking, query the package relationships recursively (or iteratively with a visited set to avoid cycles)
- Accept a `&LicensePolicy` parameter (loaded by the caller) to avoid re-reading the config file on every request
- Use the shared query helpers from `common/src/db/query.rs` if applicable for filtering
- All errors should be wrapped with `.context()` and return `Result<LicenseReport, AppError>` consistent with existing service methods

Per CONVENTIONS.md: Error handling uses `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` which follows the service pattern.

Per CONVENTIONS.md: Follow the existing module pattern where each domain module has `model/ + service/ + endpoints/` structure. Applies: task creates a new service file under `modules/fundamental/src/sbom/service/`.

## Acceptance Criteria
- Given an SBOM ID, the service returns a `LicenseReport` with packages correctly grouped by license
- Transitive dependencies are included in the groupings with `is_transitive: true`
- Each license group has the correct `compliant` flag based on the policy evaluation
- The summary accurately reflects the counts of compliant, non-compliant, and review-needed groups
- An SBOM ID that does not exist returns an appropriate error (404 equivalent)
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- Unit tests for the grouping logic (mock the database layer if possible)
- Test that packages with the same license are correctly grouped together
- Test that transitive dependencies are included
- Test compliance evaluation with mixed approved/denied licenses
- Test the summary computation
- Test error case: non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — License Policy Config (needs `LicensePolicy` for compliance evaluation)
- Depends on: Task 2 — License Report Model (needs `LicenseReport`, `LicenseGroup`, `PackageRef` structs)

[sdlc-workflow] Description digest: sha256-md:ac81b0564c933cc6688a6302df9d16a303826b08c2702d5ba05aa0c63a5de302

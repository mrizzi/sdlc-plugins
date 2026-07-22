# Task 2: Implement license compliance service with policy evaluation

- **Jira parent**: TC-9004
- **Repository**: trustify-backend
- **Target Branch**: main
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Description

Implement the service layer that generates a license compliance report for a given SBOM. The service aggregates package license data from the existing `package_license` entity, groups packages by license identifier, walks transitive dependencies to include indirect licenses, and evaluates each group against a configurable license policy.

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. No new database tables are required -- all data is aggregated from existing `package_license` and `sbom_package` entities.

## Files to Modify/Create

| Action | Path |
|---|---|
| Create | `modules/fundamental/src/sbom/service/license_report.rs` |
| Modify | `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` and expose service function |

## Implementation Notes

- **`modules/fundamental/src/sbom/service/license_report.rs`**: Implement a `generate_license_report` function (or method on `SbomService`) that:
  1. Queries `sbom_package` join table to get all packages for the given SBOM ID.
  2. Joins with `package_license` entity (`entity/src/package_license.rs`) to get license mappings.
  3. Walks transitive dependencies via the SBOM dependency graph to include indirect package licenses.
  4. Groups packages by license identifier into `LicenseGroup` structs.
  5. Loads `LicensePolicy` from a config file path (injected via app state or constructor).
  6. Evaluates each group's `compliant` flag by checking the license against the policy's allow/deny lists.
  7. Returns `Result<LicenseReport, AppError>`.
- Use `common/src/db/query.rs` query helpers for database access patterns.
- Use `common/src/error.rs` `AppError` for error wrapping with `.context()`.
- Follow the service pattern from `modules/fundamental/src/sbom/service/sbom.rs`.
- For transitive dependency resolution, query the package dependency edges stored during SBOM ingestion (see `modules/ingestor/src/graph/sbom/mod.rs` for how the SBOM graph is built).

## Acceptance Criteria

- `generate_license_report` takes an SBOM ID and returns a `LicenseReport` grouped by license.
- Transitive dependencies are included in the report (not just direct packages).
- Each `LicenseGroup` has the `compliant` field set based on the loaded `LicensePolicy`.
- All errors return `AppError` with descriptive context messages.
- Report generation meets p95 < 500ms for SBOMs with up to 1000 packages.

## Test Requirements

- Unit tests for policy evaluation logic (compliant vs. non-compliant license matching).
- Unit test for grouping logic given a flat list of (package, license) pairs.
- Unit test confirming transitive dependencies are included in the output.

## Conventions Applied

- **Module pattern**: Applies: task modifies `modules/fundamental/src/sbom/service/` matching the convention's model/service/endpoints module structure scope.
- **Error handling**: Applies: task modifies service code matching the convention's `Result<T, AppError>` with `.context()` wrapping scope.
- **Query helpers**: Applies: task modifies service code that performs database queries matching the convention's shared filtering/pagination via `common/src/db/query.rs` scope.

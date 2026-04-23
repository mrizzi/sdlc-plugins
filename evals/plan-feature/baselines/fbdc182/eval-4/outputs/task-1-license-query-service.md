## Repository
trustify-backend

## Description
Implement `LicenseReportService` inside the existing SBOM domain module. The service queries the `package_license` and `sbom_package` join tables to collect all direct and transitive package-license associations for a given SBOM, then groups them by license identifier. This is pure data-access logic; no HTTP layer is touched in this task.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — re-export the new service module

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` struct with `get_license_groups(sbom_id: Uuid, db: &DatabaseConnection) -> Result<Vec<LicenseGroup>, AppError>`

## Implementation Notes
Follow the same service pattern as `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`): a plain struct with async methods that receive a `&DatabaseConnection`, return `Result<T, AppError>`, and use `.context()` for error wrapping (see `common/src/error.rs`).

Query strategy:
- Join `entity/src/sbom_package.rs` → `entity/src/package.rs` → `entity/src/package_license.rs` using SeaORM relation traversal.
- Walk transitive dependencies by following `sbom_package` entries recursively or via a CTE; the ingestor in `modules/ingestor/src/graph/sbom/mod.rs` already stores the full dependency graph, so all packages reachable from the SBOM ID are in `sbom_package`.
- Return a `Vec<LicenseGroup>` where each entry holds the SPDX license string and the list of package purls. The `LicenseGroup` type is defined in Task 3 (license report model); add a placeholder or define it inline initially.

Use `common/src/db/query.rs` helpers for any pagination or filtering that may be required in a future extension, but for the MVP a single unbounded query is acceptable given the p95 < 500 ms target for ≤ 1000 packages.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — structural pattern to copy (struct, impl block, `&DatabaseConnection` parameter style)
- `common/src/error.rs::AppError` — error type; use `.context("license report query failed")`
- `entity/src/package_license.rs` — entity definition for the package-to-license mapping
- `entity/src/sbom_package.rs` — entity definition for the SBOM-to-package join

## Acceptance Criteria
- [ ] `LicenseReportService::get_license_groups` returns a `Vec<LicenseGroup>` grouped by SPDX license string
- [ ] All packages reachable through the SBOM's dependency graph (transitive) are included
- [ ] Packages with no license data are grouped under a sentinel value (e.g., `"NOASSERTION"`)
- [ ] The function returns `AppError` on database errors, not a panic
- [ ] `cargo build` succeeds with no new warnings

## Test Requirements
- [ ] Unit test: given a mock `DatabaseConnection` seeded with two packages under `"MIT"` and one under `"GPL-2.0"`, `get_license_groups` returns two groups with the correct package counts
- [ ] Unit test: SBOM with zero packages returns an empty `Vec`
- [ ] Unit test: package with no license entry is placed in the `"NOASSERTION"` group

## Dependencies
- Depends on: Task 3 — License report response model (defines `LicenseGroup`)

## Repository
trustify-backend

## Description
Add a `compare` method to `SbomService` that computes a structured diff between two SBOMs. The method fetches package lists, advisory associations, and license data for both SBOMs, then computes set differences for each diff category.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(&self, left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` to `SbomService`

## Implementation Notes
- Follow the service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`fetch`, `list`) for error handling with `.context()` and `Result<T, AppError>` returns.
- Use SeaORM to query `entity/src/sbom_package.rs` (join table) with `entity/src/package.rs` to get package lists for each SBOM.
- Use `entity/src/sbom_advisory.rs` with `entity/src/advisory.rs` to get advisory associations for each SBOM.
- Use `entity/src/package_license.rs` to get license data per package.
- Compute set differences using HashSet operations:
  - Added packages = right packages - left packages (by package name)
  - Removed packages = left packages - right packages
  - Version changes = packages in both with different versions
  - New vulnerabilities = right advisories - left advisories
  - Resolved vulnerabilities = left advisories - right advisories
  - License changes = packages in both with different licenses
- Return 404 via `AppError` if either SBOM ID does not exist.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods as pattern references
- `entity/src/sbom_package.rs` — SBOM-Package join table
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table
- `entity/src/package_license.rs` — Package-License mapping
- `common/src/db/query.rs` — shared query builder helpers

## Acceptance Criteria
- [ ] `SbomService::compare` returns a correct `SbomComparisonResult` for two SBOMs
- [ ] Added and removed packages are correctly identified via set difference
- [ ] Version changes detect packages present in both SBOMs with different versions
- [ ] New and resolved vulnerabilities are correctly identified
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Returns 404 if either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: two SBOMs with known differences produce correct diff categories
- [ ] Unit test: identical SBOMs produce empty diff
- [ ] Unit test: 404 for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — SBOM comparison models

# Task 3: Implement SBOM comparison service logic

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 2

## Repository

trustify-backend

## Target Branch

TC-9003

## Description

Implement the business logic that computes a structured diff between two SBOMs. The service loads package lists, advisory associations, and license data for both SBOMs from the database, then computes the six diff categories defined in the comparison model.

The comparison is computed on-the-fly from existing data (no new database tables). The service must handle SBOMs with up to 2000 packages each within the p95 < 1s latency target.

## Files to Create

- `modules/fundamental/src/sbom/service/comparison.rs` -- `SbomComparisonService` with a `compare(db: &DbConn, left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` method

## Files to Modify

- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod comparison;` declaration

## Acceptance Criteria

- [ ] `compare()` method fetches package lists for both SBOMs using existing `PackageService` queries
- [ ] Added packages: packages in right SBOM not in left (matched by package name)
- [ ] Removed packages: packages in left SBOM not in right
- [ ] Version changes: packages in both SBOMs with different versions, with correct upgrade/downgrade direction
- [ ] New vulnerabilities: advisories linked to right SBOM packages not linked to left SBOM packages
- [ ] Resolved vulnerabilities: advisories linked to left SBOM packages not linked to right SBOM packages
- [ ] License changes: packages in both SBOMs with different license values
- [ ] Returns `AppError::NotFound` if either SBOM ID does not exist
- [ ] Uses efficient set-difference operations (HashSet/HashMap) for O(n) comparison

## Test Requirements

- Unit tests with mocked database connections verifying each diff category.
- Test edge case: identical SBOMs produce an empty comparison result (all categories have zero items).
- Test edge case: one SBOM is empty (all packages appear as added or removed).

## Implementation Notes

Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs`. The method signature should accept a `&DatabaseConnection` (SeaORM) and two UUID parameters.

Use `HashSet` or `HashMap` keyed by package name for efficient diff computation. Load packages via existing entity queries from `entity/src/sbom_package.rs` and `entity/src/package.rs`. Load advisory associations via `entity/src/sbom_advisory.rs`. Load license data via `entity/src/package_license.rs`.

For version comparison direction, use semver parsing where possible; fall back to string comparison for non-semver versions.

Wrap all database query errors with `.context("description")` per the error handling convention.

## Applicable Conventions

- **Module pattern** (model/ + service/ + endpoints/): Applies: task modifies `modules/fundamental/src/sbom/service/` matching the convention's module structure scope.
- **Error handling** (Result<T, AppError> with .context()): Applies: task creates service code in `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's error handling scope.

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service logic that computes an on-the-fly diff between two SBOMs. This service fetches package and advisory data for both SBOMs using existing services and entities, then computes the six diff categories. No new database tables are needed — all computation uses existing package, advisory, and license data.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — register the comparison service function (if service module uses mod.rs for re-exports)
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`

## Implementation Notes
- Add a `compare(left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` method to `SbomService`.
- Use existing `SbomService::fetch` to load both SBOMs and validate they exist. Return `AppError::NotFound` if either SBOM ID is invalid.
- Query `sbom_package` entity (from `entity/src/sbom_package.rs`) to get the package list for each SBOM.
- Query `package_license` entity (from `entity/src/package_license.rs`) to get license mappings for each package.
- Query `sbom_advisory` entity (from `entity/src/sbom_advisory.rs`) to get advisory associations for each SBOM.
- Use `AdvisoryService::fetch` or direct entity queries to get severity information for advisories.
- Compute diffs using set operations on package names:
  - **Added packages**: packages in right but not in left (by package name/version key)
  - **Removed packages**: packages in left but not in right
  - **Version changes**: packages present in both but with different versions; compute direction by semver comparison
  - **New vulnerabilities**: advisories associated with right SBOM but not left
  - **Resolved vulnerabilities**: advisories associated with left SBOM but not right
  - **License changes**: packages present in both where the license field differs
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries rather than per-package lookups. Consider using `HashSet` or `HashMap` for O(1) lookups during diff computation.
- Follow error handling pattern from existing service methods: `Result<T, AppError>` with `.context()` wrapping on database operations.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with `fetch` and `list` methods; add `compare` here
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisory details including severity
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package details including license
- `entity/src/sbom_package.rs` — SBOM-to-package join table for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-to-advisory join table for querying vulnerabilities per SBOM
- `entity/src/package_license.rs` — package-to-license mapping for license change detection
- `common/src/error.rs::AppError` — error handling pattern for service methods
- `common/src/db/query.rs` — shared query builder helpers for batch data fetching

## Acceptance Criteria
- [ ] `SbomService::compare` method computes correct diffs for all six categories
- [ ] Returns `AppError::NotFound` when either SBOM ID does not exist
- [ ] Handles edge case of identical SBOMs (all diff categories empty)
- [ ] Handles edge case of SBOMs with no packages (empty diff)
- [ ] Performance: p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences and verify added/removed/changed counts
- [ ] Unit test: compare identical SBOMs and verify all diff categories are empty
- [ ] Unit test: compare with invalid SBOM ID returns NotFound error
- [ ] Unit test: verify version change direction (upgrade vs downgrade) is computed correctly
- [ ] Unit test: verify license changes are detected when package license differs between SBOMs
- [ ] Unit test: verify new and resolved vulnerabilities are correctly identified

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 2 — Backend comparison response model

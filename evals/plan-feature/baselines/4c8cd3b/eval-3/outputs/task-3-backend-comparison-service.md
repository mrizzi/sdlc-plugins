## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service function that computes the structured diff between two SBOMs. The service fetches package and advisory data for both SBOMs, then computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This is the core business logic for the comparison feature, computed on-the-fly without new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `compare_sboms(db, left_id, right_id) -> Result<SbomComparisonResult, AppError>` function

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the comparison service module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the function should accept a database connection and two SBOM IDs, returning `Result<SbomComparisonResult, AppError>`.
- Use the existing `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch packages for each SBOM. Use the existing `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories linked to each SBOM.
- Use the SeaORM entity relationships defined in `entity/src/sbom_package.rs` (SBOM-Package join) and `entity/src/sbom_advisory.rs` (SBOM-Advisory join) to query packages and advisories per SBOM.
- Use `entity/src/package_license.rs` to resolve license information for each package.
- Diff computation approach:
  1. Fetch all packages for the left SBOM and right SBOM into HashMaps keyed by package name.
  2. Added packages = keys in right but not in left. Removed packages = keys in left but not in right.
  3. Version changes = keys in both where version differs. Determine direction by comparing semver if parseable, otherwise default to "upgrade".
  4. Fetch advisories for both SBOMs. New vulnerabilities = advisories affecting right but not left. Resolved = advisories affecting left but not right.
  5. License changes = packages in both where the license field differs.
- Wrap all database errors with `.context()` using the pattern from `common/src/error.rs::AppError`.
- Performance: the non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries rather than N+1 queries — fetch all packages for an SBOM in a single query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern for database access and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch packages for a given SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories linked to an SBOM
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type and `.context()` wrapping pattern

## Acceptance Criteria
- [ ] `compare_sboms` function accepts two SBOM IDs and returns `SbomComparisonResult`
- [ ] Added packages are correctly identified (in right SBOM, not in left)
- [ ] Removed packages are correctly identified (in left SBOM, not in right)
- [ ] Version changes are detected with correct direction (upgrade/downgrade)
- [ ] New vulnerabilities are identified (advisories affecting right but not left)
- [ ] Resolved vulnerabilities are identified (advisories affecting left but not right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Returns appropriate error when either SBOM ID does not exist
- [ ] No new database tables or migrations are created (per non-functional requirements)

## Test Requirements
- [ ] Unit test: two SBOMs with non-overlapping packages — all left packages appear as removed, all right packages as added
- [ ] Unit test: two SBOMs with overlapping packages at different versions — version changes are detected with correct direction
- [ ] Unit test: two SBOMs where the right SBOM has a new advisory — new vulnerability is reported
- [ ] Unit test: two SBOMs where the left SBOM has an advisory not in right — resolved vulnerability is reported
- [ ] Unit test: package with different license between SBOMs — license change is reported
- [ ] Unit test: identical SBOMs — all diff sections are empty
- [ ] Unit test: non-existent SBOM ID returns an error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model structs

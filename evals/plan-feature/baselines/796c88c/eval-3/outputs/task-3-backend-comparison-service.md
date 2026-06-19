## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the comparison service that computes the structured diff between two SBOMs. The service takes two SBOM IDs, fetches their package lists and associated advisories from the database, and computes the six diff categories: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This is the core business logic for the SBOM comparison feature.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` — `SbomComparisonService` with a `compare(left_id, right_id) -> Result<SbomComparison, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs`. The comparison service should:

1. Accept a database connection/pool and two SBOM IDs (UUIDs).
2. Use `SbomService` to fetch both SBOM details and verify they exist (return 404 `AppError` if either is missing).
3. Use `PackageService` to fetch the full package list for each SBOM, keyed by package name.
4. Compute diffs:
   - **Added packages**: packages in right but not in left
   - **Removed packages**: packages in left but not in right
   - **Version changes**: packages in both but with different versions; determine `direction` by comparing semver (or lexicographic if not valid semver)
   - **New vulnerabilities**: advisories linked to right SBOM packages that are not linked to left SBOM packages
   - **Resolved vulnerabilities**: advisories linked to left SBOM packages that are not linked to right SBOM packages
   - **License changes**: packages in both where the license string differs
5. For each advisory, include `severity` from `AdvisorySummary`.
6. Return `SbomComparison` struct.

Use `HashMap` for O(1) lookups when comparing package lists. No new database tables or migrations needed -- compute everything on-the-fly from existing entities.

Performance: for SBOMs with up to 2000 packages each, the diff should complete within the p95 < 1s budget. Use batch queries rather than N+1 fetches.

Error handling: use `Result<T, AppError>` with `.context()` wrapping per project conventions.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Use to fetch SBOM details by ID
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Use to fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Use to fetch advisories linked to packages
- `common/src/error.rs::AppError` — Error type for service results
- `common/src/db/query.rs` — Query builder helpers for batch fetching

## Acceptance Criteria
- [ ] `SbomComparisonService::compare()` correctly computes all six diff categories
- [ ] Returns `AppError::NotFound` if either SBOM ID does not exist
- [ ] Handles edge cases: identical SBOMs (all diff lists empty), one SBOM has no packages, disjoint package sets
- [ ] Uses batch queries to avoid N+1 performance issues
- [ ] Module is exported from `modules/fundamental/src/sbom/service/mod.rs`

## Test Requirements
- [ ] Unit test: identical SBOMs produce empty diffs
- [ ] Unit test: completely disjoint SBOMs produce correct added/removed lists
- [ ] Unit test: version changes are correctly classified as upgrade/downgrade
- [ ] Unit test: license changes are detected when package exists in both but license differs
- [ ] Unit test: vulnerabilities are correctly categorized as new or resolved

## Dependencies
- Depends on: Task 2 — Backend comparison model

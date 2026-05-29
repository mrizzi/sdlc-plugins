# Task 3 — Add SBOM comparison diff service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the service-layer logic that computes a structured diff between two SBOMs. The service fetches package lists, advisories, and licenses for both SBOMs from existing data, then computes the six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes). The diff is computed on-the-fly — no new database tables are needed.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add a `compare` method to `SbomService` that accepts two SBOM IDs and returns `SbomComparisonResult`
- `modules/fundamental/src/sbom/service/mod.rs` — Ensure the compare method is accessible

## Implementation Notes
- Add a `pub async fn compare(&self, left_id: Id, right_id: Id) -> Result<SbomComparisonResult, AppError>` method to `SbomService`.
- Use the existing `SbomService` fetch methods to load both SBOMs and their associated data.
- Use `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) to fetch the package list for each SBOM.
- Use `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`) to fetch advisories linked to each SBOM via the `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`).
- Use `package_license` entity (see `entity/src/package_license.rs`) to resolve license information per package.
- Diff computation approach:
  1. Build a `HashMap<package_name, PackageInfo>` for each SBOM's packages.
  2. Added packages = keys in right but not in left.
  3. Removed packages = keys in left but not in right.
  4. Version changes = keys in both where version differs. Direction = "upgrade" if right version > left version, "downgrade" otherwise.
  5. New vulnerabilities = advisories in right SBOM's set but not in left's.
  6. Resolved vulnerabilities = advisories in left SBOM's set but not in right's.
  7. License changes = packages in both where the license field differs.
- Follow the error handling pattern used in existing service methods: `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`.
- Non-functional: the comparison must handle SBOMs with up to 2000 packages each with p95 < 1s. Using HashMaps for set difference operations achieves this.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods to reuse for loading SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories linked to SBOMs
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error handling enum for consistent error responses

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method exists and returns `SbomComparisonResult`
- [ ] Added packages are correctly identified (present in right, absent in left)
- [ ] Removed packages are correctly identified (present in left, absent in right)
- [ ] Version changes are detected with correct upgrade/downgrade direction
- [ ] New vulnerabilities are identified (advisories in right SBOM not in left)
- [ ] Resolved vulnerabilities are identified (advisories in left SBOM not in right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Method returns `AppError` for invalid SBOM IDs (not found)

## Test Requirements
- [ ] Test comparison with two SBOMs that have added, removed, and changed packages
- [ ] Test comparison where one SBOM has a vulnerability the other does not
- [ ] Test comparison with license changes between SBOMs
- [ ] Test error case: comparing with a non-existent SBOM ID returns an appropriate error
- [ ] Test edge case: comparing an SBOM with itself returns empty diff categories

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model structs

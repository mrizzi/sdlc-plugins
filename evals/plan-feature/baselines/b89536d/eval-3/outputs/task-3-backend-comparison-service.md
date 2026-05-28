# Task 3 — Add SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the service layer logic that computes a structured diff between two SBOMs. The service fetches package, advisory, and license data for both SBOMs from existing services, then computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` with a `compare(left_id, right_id) -> Result<SbomComparison, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the comparison service module

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) — the comparison service should accept the same database connection/pool type and return `Result<T, AppError>` with `.context()` error wrapping per `common/src/error.rs`.
- Use existing `SbomService` to fetch SBOM details for both IDs. Use `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) to list packages for each SBOM. Use `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`) to list advisories affecting each SBOM.
- Diff algorithm for packages: build a `HashMap<package_name, PackageInfo>` for each SBOM. Packages in right but not left are "added". Packages in left but not right are "removed". Packages in both with different versions are "version changes" (compare semver to determine "upgrade" vs "downgrade").
- Diff algorithm for vulnerabilities: collect advisory IDs for each SBOM. Advisories in right but not left are "new vulnerabilities". Advisories in left but not right are "resolved vulnerabilities".
- Diff algorithm for licenses: for packages present in both SBOMs, compare license fields. Differences are "license changes".
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashSet/HashMap) rather than nested iteration.
- Return an `AppError` with appropriate HTTP status if either SBOM ID is not found (404).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM data; reuse its methods to load SBOM details and associated packages
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for fetching package data per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for fetching advisories; reuse to load advisory data for each SBOM
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type for consistent error handling

## Acceptance Criteria
- [ ] `SbomCompareService::compare(left_id, right_id)` returns a correctly populated `SbomComparison`
- [ ] Added packages are correctly identified (in right but not left)
- [ ] Removed packages are correctly identified (in left but not right)
- [ ] Version changes correctly identify upgrade vs downgrade direction
- [ ] New vulnerabilities are correctly identified (advisories in right but not left)
- [ ] Resolved vulnerabilities are correctly identified (advisories in left but not right)
- [ ] License changes are correctly identified for packages present in both SBOMs
- [ ] Returns 404 AppError if either SBOM ID is not found
- [ ] Diff computation completes within performance target for large SBOMs

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — verify all six diff categories
- [ ] Integration test: compare an SBOM with itself — all diff sections should be empty
- [ ] Integration test: compare with a non-existent SBOM ID — should return 404
- [ ] Unit test: version change direction detection (upgrade and downgrade cases)
- [ ] Unit test: empty SBOM comparison (both SBOMs have zero packages)

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model types

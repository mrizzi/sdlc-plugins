# Task 3 — Add SBOM comparison diff service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the core diffing logic that compares two SBOMs and produces a structured `SbomComparisonResult`. The service computes the diff on-the-fly from existing package, advisory, and license data without creating new database tables. It identifies added/removed packages, version changes, new/resolved vulnerabilities, and license changes between the two SBOMs.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` (or a `compare` method on existing `SbomService`) with the diff computation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` or expose the comparison method on `SbomService`

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` for method signatures, error handling (`Result<T, AppError>` with `.context()` wrapping), and database interaction patterns.
- Use SeaORM queries to load packages for each SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`), then compute the diff in memory.
- For package comparison: load all packages for the left SBOM and right SBOM, compare by package name to find added (right-only), removed (left-only), and version-changed (both sides, different version) entries.
- For vulnerability comparison: load advisories linked to each SBOM via `sbom_advisory` join table (`entity/src/sbom_advisory.rs`), diff by advisory ID to find new (right-only) and resolved (left-only) vulnerabilities.
- For license comparison: use the `package_license` entity (`entity/src/package_license.rs`) to find packages where the license changed between the two SBOMs.
- The `direction` field in `VersionChange` should compare semantic versions when possible, defaulting to string comparison. Use "upgrade" when right version is newer, "downgrade" otherwise.
- Non-functional requirement: p95 response time < 1s for SBOMs with up to 2000 packages each. Optimize by loading all data in bulk queries rather than N+1 queries.
- Use `common/src/db/query.rs` for any query builder helpers needed.
- Error handling: return appropriate `AppError` variants for invalid SBOM IDs (not found).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with database query patterns for SBOM operations
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — advisory query patterns including severity field access
- `modules/fundamental/src/package/service/mod.rs::PackageService` — package query patterns including license field access
- `common/src/db/query.rs` — shared query builder helpers (filtering, pagination, sorting)
- `common/src/error.rs::AppError` — error enum for consistent error handling

## Acceptance Criteria
- [ ] Comparison service accepts two SBOM IDs and returns a populated `SbomComparisonResult`
- [ ] Added packages are correctly identified (present in right SBOM but not left)
- [ ] Removed packages are correctly identified (present in left SBOM but not right)
- [ ] Version changes are correctly identified with upgrade/downgrade direction
- [ ] New vulnerabilities are identified (advisories affecting right SBOM but not left)
- [ ] Resolved vulnerabilities are identified (advisories affecting left SBOM but not right)
- [ ] License changes are identified for packages present in both SBOMs
- [ ] Returns appropriate error when an SBOM ID does not exist
- [ ] No new database tables or migrations are created — all data is computed from existing entities

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences, verify added/removed/changed counts
- [ ] Unit test: compare identical SBOMs, verify all diff sections are empty
- [ ] Unit test: verify version direction detection (upgrade vs downgrade)
- [ ] Unit test: verify vulnerability diff correctness (new vs resolved)
- [ ] Unit test: verify license change detection
- [ ] Unit test: verify error handling for invalid SBOM IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model structs

[sdlc-workflow] Description digest: sha256:8f1e5104b609265b14213e77c89be48a24473db9e8dc678d5a7d75d31fa8a89a

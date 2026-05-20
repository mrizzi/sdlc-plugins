# Task 3 — Add SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the diff computation logic in `SbomService` that takes two SBOM IDs and produces a structured `SbomComparisonResult`. The service fetches both SBOMs' package lists and associated advisories, then computes the six diff categories: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id)` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (fetch, list, ingest) — the compare method should accept a database connection/pool and return `Result<SbomComparisonResult, AppError>`
- Use `.context()` wrapping on all fallible operations per the error handling convention (see `common/src/error.rs` for the `AppError` enum)
- Algorithm outline:
  1. Fetch both SBOMs by ID using existing `SbomService::fetch` (return 404 if either does not exist)
  2. Fetch package lists for both SBOMs via `PackageService` or direct entity queries on `sbom_package` join table
  3. Build hash maps keyed by package name for O(n) comparison
  4. Compute added packages (in right but not left), removed packages (in left but not right), version changes (in both but different version)
  5. For version changes, determine direction by comparing version strings (consider using semver parsing if available, otherwise string comparison)
  6. Fetch advisories for both SBOMs via `AdvisoryService` or `sbom_advisory` join table
  7. Compute new vulnerabilities (advisories affecting right but not left) and resolved vulnerabilities (advisories affecting left but not right)
  8. Compare license fields on packages present in both SBOMs to detect license changes
- Performance: the non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries rather than per-package lookups. Consider fetching all packages and advisories in two bulk queries per SBOM
- No new database tables — compute everything from existing `sbom`, `package`, `sbom_package`, `advisory`, `sbom_advisory`, and `package_license` entities

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch/list methods for loading SBOM data
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing fetch/list/search methods for loading advisory data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing fetch/list methods for loading package data
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for package lookups
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for advisory lookups
- `entity/src/package_license.rs` — Package-License mapping entity for license comparisons

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method implemented and returns `Result<SbomComparisonResult, AppError>`
- [ ] Returns 404 error if either SBOM ID does not exist
- [ ] Correctly identifies added packages (in right but not left)
- [ ] Correctly identifies removed packages (in left but not right)
- [ ] Correctly identifies version changes with upgrade/downgrade direction
- [ ] Correctly identifies new vulnerabilities (advisories in right but not left)
- [ ] Correctly identifies resolved vulnerabilities (advisories in left but not right)
- [ ] Correctly identifies license changes for packages present in both SBOMs
- [ ] No new database tables or migrations created

## Test Requirements
- [ ] Integration test: compare two SBOMs where right has additional packages — verify added_packages populated correctly
- [ ] Integration test: compare two SBOMs where left has packages removed in right — verify removed_packages populated correctly
- [ ] Integration test: compare two SBOMs where a shared package has a different version — verify version_changes with correct direction
- [ ] Integration test: compare two SBOMs where right introduces a new advisory — verify new_vulnerabilities populated
- [ ] Integration test: compare two SBOMs where left has an advisory resolved in right — verify resolved_vulnerabilities populated
- [ ] Integration test: compare two SBOMs where a package's license changed — verify license_changes populated
- [ ] Integration test: return 404 when left SBOM ID does not exist
- [ ] Integration test: return 404 when right SBOM ID does not exist
- [ ] Integration test: compare identical SBOMs — verify all diff sections are empty

## Verification Commands
- `cargo test --package trustify-fundamental -- sbom::service::compare` — all comparison service tests pass

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model structs

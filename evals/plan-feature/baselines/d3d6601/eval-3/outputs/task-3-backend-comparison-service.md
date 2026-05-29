## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison service that computes a structured diff between two SBOMs. The service fetches the package lists and associated advisory data for both SBOMs, then computes set differences to produce the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables required.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` — `SbomComparisonService` with `compare(left_id, right_id)` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod comparison;` to expose the new service module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the service takes a database connection and returns `Result<SbomComparison, AppError>`.
- Use `AppError` from `common/src/error.rs` for error handling, wrapping database errors with `.context()`.
- The `compare` method should:
  1. Fetch packages for both SBOMs using `PackageService` or direct queries on the `sbom_package` join table (entity at `entity/src/sbom_package.rs`).
  2. Compute set difference by package name: packages in right but not left = added, packages in left but not right = removed.
  3. For packages present in both, compare versions — differing versions produce `VersionChange` entries with direction computed by semver comparison (or string comparison as fallback).
  4. Fetch advisories for both SBOMs via the `sbom_advisory` join table (entity at `entity/src/sbom_advisory.rs`) and compute new/resolved vulnerabilities by advisory ID set difference.
  5. Compare licenses for packages present in both SBOMs — differing licenses produce `LicenseChange` entries using the `package_license` entity at `entity/src/package_license.rs`.
- Return 404 with a descriptive message if either SBOM ID does not exist.
- The p95 response time requirement is <1s for SBOMs with up to 2000 packages. Use efficient set operations (HashSet-based lookups) rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reuse its database connection pattern and error handling approach
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for advisory data fetching pattern
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for package data fetching pattern
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for consistent error responses

## Acceptance Criteria
- [ ] `SbomComparisonService::compare(left_id, right_id)` returns a correctly populated `SbomComparison` struct
- [ ] Added packages are correctly identified (in right but not in left)
- [ ] Removed packages are correctly identified (in left but not in right)
- [ ] Version changes are detected for packages present in both SBOMs with different versions
- [ ] New vulnerabilities are advisories affecting right SBOM but not left
- [ ] Resolved vulnerabilities are advisories affecting left SBOM but not right
- [ ] License changes are detected for packages present in both with different licenses
- [ ] Returns 404 error if either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: compare two SBOMs where the right has additional packages — verify `added_packages` is populated correctly
- [ ] Unit test: compare two SBOMs where the left has packages removed in right — verify `removed_packages` is populated
- [ ] Unit test: compare two SBOMs with version changes — verify direction field is correct (upgrade vs downgrade)
- [ ] Unit test: compare two SBOMs with different advisory associations — verify new and resolved vulnerabilities
- [ ] Unit test: compare with non-existent SBOM ID — verify 404 error

## Verification Commands
- `cargo test -p trustify-fundamental -- sbom::service::comparison` — run comparison service tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison response model types

[sdlc-workflow] Description digest: sha256:756a4902313d9ae5f2ab586a84b611f7a4ca4c5ccf6111c9b2b878d51583039b

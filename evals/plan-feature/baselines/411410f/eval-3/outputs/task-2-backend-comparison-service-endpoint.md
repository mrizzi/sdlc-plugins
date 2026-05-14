# Task 2: Implement SBOM comparison service and endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core diffing logic as a comparison service and expose it via a new `GET /api/v2/sbom/compare?left={id}&right={id}` endpoint. The service fetches package and advisory data for both SBOMs from existing service layers, computes the diff across all six categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes), and returns an `SbomComparison` response. No new database tables are required — the diff is computed on-the-fly.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomComparisonService` with a `compare(left_id, right_id)` method that computes the structured diff
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` that extracts query params, validates both IDs exist, calls the service, and returns JSON

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to register the comparison service submodule
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM router, following the same pattern as `list.rs` and `get.rs` route registration

## Implementation Notes
- **Service layer** (`service/compare.rs`):
  - Follow the pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the service takes a database connection reference and returns `Result<SbomComparison, AppError>`.
  - Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch packages for each SBOM. The `sbom_package` join entity (`entity/src/sbom_package.rs`) links SBOMs to packages.
  - Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories. The `sbom_advisory` join entity (`entity/src/sbom_advisory.rs`) links SBOMs to advisories.
  - Use `package_license` entity (`entity/src/package_license.rs`) for license data.
  - Compute added/removed packages by comparing package name sets between left and right SBOMs using `HashSet` difference operations.
  - For version changes, find packages present in both SBOMs with different version strings. Determine direction by attempting semver comparison (use the `semver` crate); fall back to `Unknown` if versions are not valid semver.
  - For vulnerability diffs, compare advisory ID sets between left and right SBOMs.
  - For license changes, compare the license field on packages present in both SBOMs.
  - Use `AppError` from `common/src/error.rs` for error handling with `.context()` wrapping.
- **Endpoint** (`endpoints/compare.rs`):
  - Define a query params struct: `SbomCompareQuery { left: Uuid, right: Uuid }` with Axum `Query` extractor.
  - Validate that `left != right` (return 400 Bad Request if identical).
  - Validate both SBOM IDs exist using `SbomService::fetch()` from `modules/fundamental/src/sbom/service/sbom.rs` (return 404 if not found).
  - Call `SbomComparisonService::compare()` and return `Json(comparison)`.
  - Follow the error handling pattern in existing endpoints like `modules/fundamental/src/sbom/endpoints/get.rs`.
- **Route registration** in `endpoints/mod.rs`:
  - Add `.route("/compare", get(compare::compare_sboms))` to the SBOM router, following the existing patterns for `list` and `get` routes.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id}&right={id}` returns a 200 response with a valid `SbomComparison` JSON body
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Returns 400 if `left` and `right` are the same ID
- [ ] Returns 400 if query parameters are missing
- [ ] Added/removed packages are correctly computed as set differences
- [ ] Version changes correctly detect upgrade vs downgrade using semver
- [ ] New/resolved vulnerabilities are correctly computed from advisory associations
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Response time is under 1s for SBOMs with up to 2000 packages each (p95 target)

## Test Requirements
- [ ] Unit test for the comparison service with mock package/advisory data covering all six diff categories
- [ ] Unit test for version direction detection (semver upgrade, downgrade, non-semver fallback to Unknown)
- [ ] Unit test for edge case: two identical SBOMs produce an empty diff (all arrays empty)
- [ ] Unit test for edge case: one SBOM has zero packages

## Dependencies
- Depends on: Task 1 — Define SBOM comparison response model

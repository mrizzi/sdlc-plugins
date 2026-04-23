## Repository
trustify-backend

## Description
Implement the comparison service logic and HTTP endpoint that computes a structured diff between two SBOMs. The service loads packages and advisories for both SBOMs from existing entity tables, computes set differences (added/removed packages, version changes, vulnerability diffs, license changes), and returns the result as an `SbomComparison` struct. The endpoint is registered at `GET /api/v2/sbom/compare?left={id1}&right={id2}`.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare()` method implementation that queries packages and advisories for both SBOMs and computes the diff
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` that validates query params, calls the service, and returns the JSON response

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the comparison service module
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing `/api/v2/sbom` routes
- `server/src/main.rs` — No changes needed if route registration follows the existing pattern in `endpoints/mod.rs`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparison` JSON with six diff sections. Returns 400 if either ID is missing or invalid, 404 if either SBOM is not found.

## Implementation Notes
- **Service layer** (`compare.rs`): Follow the pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` methods take a database connection and return `Result<T, AppError>`. The compare method should:
  1. Fetch packages for both SBOMs by joining `entity/src/sbom_package.rs` with `entity/src/package.rs` and `entity/src/package_license.rs`
  2. Fetch advisories for both SBOMs by joining `entity/src/sbom_advisory.rs` with `entity/src/advisory.rs`
  3. Compute set differences using HashMaps keyed by package name
  4. For version changes, compare packages present in both sets but with different versions; determine direction by semver comparison
  5. For vulnerability diffs, compare advisory sets between the two SBOMs
  6. For license changes, compare license fields of packages present in both SBOMs
- **Performance**: Use batch queries (WHERE sbom_id IN (left, right)) rather than separate queries per SBOM. This is critical for the p95 < 1s requirement with up to 2000 packages per SBOM.
- **Endpoint layer** (`compare.rs`): Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` — extract query parameters using `axum::extract::Query`, call the service, return `Json<SbomComparison>`. Use `AppError` from `common/src/error.rs` for error responses.
- **Route registration**: In `modules/fundamental/src/sbom/endpoints/mod.rs`, add `.route("/compare", get(compare::handler))` following the existing pattern for `list.rs` and `get.rs`.
- **Query helpers**: Use `common/src/db/query.rs` for any filtering or pagination of results if needed.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the `compare` method
- `modules/fundamental/src/sbom/endpoints/get.rs` — pattern for endpoint handler structure and error handling
- `common/src/error.rs::AppError` — error type for 400/404 responses
- `entity/src/sbom_package.rs` — join table for SBOM-to-package relationships
- `entity/src/sbom_advisory.rs` — join table for SBOM-to-advisory relationships
- `entity/src/package_license.rs` — package-to-license mapping for license change detection

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid `SbomComparison` JSON body
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Added packages are correctly identified (present in right, absent in left)
- [ ] Removed packages are correctly identified (present in left, absent in right)
- [ ] Version changes include correct left/right versions and upgrade/downgrade direction
- [ ] New vulnerabilities are correctly identified (advisories in right SBOM not in left)
- [ ] Resolved vulnerabilities are correctly identified (advisories in left SBOM not in right)
- [ ] License changes are correctly detected for packages present in both SBOMs
- [ ] Response time < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — verify all six diff sections contain expected entries
- [ ] Integration test: compare an SBOM with itself — all diff sections should be empty
- [ ] Integration test: request with missing `left` param returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: compare SBOMs with overlapping packages but different versions — verify `version_changes` and `direction` field

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-tests sbom_compare` — integration tests pass

## Dependencies
- Depends on: Task 1 — SBOM comparison model

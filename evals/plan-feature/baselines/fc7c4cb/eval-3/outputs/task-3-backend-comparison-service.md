## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add a comparison method to the SBOM service that computes a structured diff between two SBOMs. The method loads package and advisory data for both SBOMs, computes set differences for packages, identifies version changes, correlates advisories to find new and resolved vulnerabilities, and detects license changes. The diff is computed on-the-fly from existing data without requiring new database tables.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id)` method to `SbomService` that returns `Result<SbomComparisonResult, AppError>`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` — methods take `&self` and a connection/transaction reference, return `Result<T, AppError>` with `.context()` error wrapping.
- Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch packages for each SBOM. Use the existing query helpers from `common/src/db/query.rs` for filtering packages by SBOM ID.
- Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisories correlated with each SBOM via the `sbom_advisory` join table (entity defined in `entity/src/sbom_advisory.rs`).
- Use the `package_license` entity from `entity/src/package_license.rs` to look up license data for license change detection.
- Algorithm for comparison:
  1. Fetch all packages for left SBOM and right SBOM using `sbom_package` join table (`entity/src/sbom_package.rs`).
  2. Build hash maps keyed by package name for set operations.
  3. Added packages = in right but not in left. Removed packages = in left but not in right.
  4. Version changes = in both but with different version strings. Direction = "upgrade" if right version > left version (semver comparison), else "downgrade".
  5. For advisories: fetch advisory sets for each SBOM. New vulnerabilities = advisories in right SBOM not in left. Resolved = in left not in right.
  6. License changes = packages in both SBOMs where license string differs.
- Performance: the non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages each. Use bulk queries rather than N+1 patterns. Load all packages and advisories in two queries per SBOM, then compute diffs in memory.
- Reference the error handling pattern from `common/src/error.rs` — use `AppError` enum and `.context()` wrapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend this existing service with the new comparison method rather than creating a separate service
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for fetching packages; reuse for loading package data per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for fetching advisories; reuse for loading advisory data per SBOM
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for SBOM-scoped package/advisory queries
- `entity/src/sbom_package.rs` — existing join table entity for SBOM-to-package relationships
- `entity/src/sbom_advisory.rs` — existing join table entity for SBOM-to-advisory relationships

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method exists and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added packages are correctly identified (present in right, absent in left)
- [ ] Removed packages are correctly identified (present in left, absent in right)
- [ ] Version changes are detected with correct direction (upgrade/downgrade)
- [ ] New vulnerabilities are identified (advisories in right SBOM not in left)
- [ ] Resolved vulnerabilities are identified (advisories in left SBOM not in right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Method returns appropriate error when either SBOM ID does not exist
- [ ] Performance is acceptable for SBOMs with up to 2000 packages (no N+1 queries)

## Test Requirements
- [ ] Integration test: compare two SBOMs where the right SBOM has additional packages — verify added packages list is correct
- [ ] Integration test: compare two SBOMs where the left SBOM has packages removed in the right — verify removed packages list
- [ ] Integration test: compare two SBOMs with a package present in both but with different versions — verify version change with correct direction
- [ ] Integration test: compare two SBOMs with different advisory sets — verify new and resolved vulnerabilities
- [ ] Integration test: compare two SBOMs where a package's license changed — verify license changes
- [ ] Integration test: compare with a non-existent SBOM ID — verify error response
- [ ] Integration test: compare two identical SBOMs — verify all diff categories are empty

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model types

[sdlc-workflow] Description digest: sha256:b95bededd002039e67e82d6c455f35f6142464080e3db26917c9358ac9b4abe4

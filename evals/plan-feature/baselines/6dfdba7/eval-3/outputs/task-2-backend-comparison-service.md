## Repository
trustify-backend

## Description
Implement the core diff logic that compares two SBOMs and produces an `SbomComparison` result. This service function loads the package lists, advisories, and license data for two SBOMs from the database, then computes the six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes). This is the business logic layer that the endpoint handler will call.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` -- `SbomCompareService` (or a method on the existing `SbomService`) that accepts two SBOM IDs and returns `Result<SbomComparison, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod compare;` to register the new submodule

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs`. The existing `SbomService` takes a database connection and provides methods like `fetch` and `list`. Either add a `compare` method to `SbomService` or create a standalone `compare_sboms` function that takes a `DatabaseConnection` reference and two SBOM IDs.
- To compute the diff:
  1. Load packages for both SBOMs using the `sbom_package` join table (`entity/src/sbom_package.rs`) and `package` entity (`entity/src/package.rs`). Key packages by name for O(n) set operations.
  2. Added packages = packages in right but not in left. Removed packages = packages in left but not in right.
  3. Version changes = packages present in both but with different versions. Determine direction by comparing version strings (semver comparison if possible, lexicographic fallback).
  4. For vulnerability diffs, load advisories linked to each SBOM via `sbom_advisory` join table (`entity/src/sbom_advisory.rs`). New vulnerabilities = advisories in right but not in left. Resolved = advisories in left but not in right.
  5. License changes = packages present in both with different license values. Use the `package_license` entity (`entity/src/package_license.rs`).
- Use `common/src/db/query.rs` query helpers for database access patterns.
- Wrap all database errors with `.context()` per the project's error handling pattern in `common/src/error.rs`.
- Performance: the requirement is p95 <1s for SBOMs up to 2000 packages. Load both package lists in parallel using `tokio::try_join!` to minimize latency. Avoid N+1 queries -- batch-load advisories for all relevant packages.
- No new database tables are needed -- compute everything from existing entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Pattern for database access, connection handling, and error wrapping
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Package query patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- Advisory query patterns
- `entity/src/sbom_package.rs` -- SBOM-to-Package join entity for loading package lists
- `entity/src/sbom_advisory.rs` -- SBOM-to-Advisory join entity for loading advisory associations
- `entity/src/package_license.rs` -- Package-to-License mapping for license comparison
- `common/src/db/query.rs` -- Shared query builder helpers

## Acceptance Criteria
- [ ] A function or method exists that accepts two SBOM IDs and returns `Result<SbomComparison, AppError>`
- [ ] Added packages are correctly computed (in right, not in left)
- [ ] Removed packages are correctly computed (in left, not in right)
- [ ] Version changes detect packages with the same name but different versions, with correct upgrade/downgrade direction
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes detect packages with the same name but different license values
- [ ] Returns appropriate error when either SBOM ID does not exist
- [ ] No new database tables or migrations are created

## Test Requirements
- [ ] Unit test: two SBOMs with no overlap produce all packages as added/removed
- [ ] Unit test: identical SBOMs produce empty diff in all categories
- [ ] Unit test: version change with higher right version reports `Upgrade`, lower reports `Downgrade`
- [ ] Unit test: advisory present only in right SBOM appears in `new_vulnerabilities`
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Verification Commands
- `cargo test -p trustify-fundamental compare` -- should pass all comparison service tests

## Dependencies
- Depends on: Task 1 -- Define SBOM comparison model types

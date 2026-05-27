# Task 3 — Add SBOM comparison diffing service logic

**Summary:** Add SBOM comparison diffing service logic

**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the comparison diffing logic in the SBOM service layer. This function takes two SBOM IDs, loads their package and advisory data from the database, computes the structured diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes), and returns an `SbomComparisonResult`. The diffing is computed on-the-fly from existing data — no new database tables are introduced.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — comparison logic: `compare_sboms(db, left_id, right_id) -> Result<SbomComparisonResult, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` to expose the comparison service module

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the function should accept a database connection reference and return `Result<T, AppError>` with `.context()` wrapping for error handling.
- Use SeaORM queries to load packages for both SBOMs via the `sbom_package` join table (`entity/src/sbom_package.rs`), and advisories via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).
- Use the `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` (includes license field) to build package-level diff data.
- Use the `AdvisorySummary` struct from `modules/fundamental/src/advisory/model/summary.rs` (includes severity field) to build vulnerability diff data.
- Diffing algorithm:
  1. Load all packages for left SBOM and right SBOM
  2. Compute added packages (in right but not left, matched by package name)
  3. Compute removed packages (in left but not right)
  4. Compute version changes (in both but different versions; determine upgrade/downgrade by comparing version strings)
  5. Load advisories for both SBOMs; compute new vulnerabilities (affecting right but not left) and resolved vulnerabilities (affecting left but not right)
  6. Compute license changes (same package, different license between left and right)
- Use shared query helpers from `common/src/db/query.rs` for database query construction.
- Per non-functional requirements: target p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashMaps keyed by package name) rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference for service function patterns, database connection handling, and error wrapping
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for consistent error handling
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping for license change detection

## Acceptance Criteria
- [ ] `compare_sboms` function accepts two SBOM IDs and returns `SbomComparisonResult`
- [ ] Added packages are correctly identified (in right SBOM but not in left)
- [ ] Removed packages are correctly identified (in left SBOM but not in right)
- [ ] Version changes are detected with correct upgrade/downgrade direction
- [ ] New vulnerabilities are identified (advisories affecting right but not left)
- [ ] Resolved vulnerabilities are identified (advisories affecting left but not right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Returns appropriate error when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: two identical SBOMs produce empty diff (all vectors empty)
- [ ] Unit test: SBOM with additional packages shows them in added_packages
- [ ] Unit test: SBOM with removed packages shows them in removed_packages
- [ ] Unit test: Package version change is detected with correct direction
- [ ] Unit test: New and resolved vulnerabilities are correctly computed
- [ ] Unit test: License change between same package is detected
- [ ] Unit test: non-existent SBOM ID returns appropriate error

## Dependencies
- Depends on: Task 2 — Add SBOM comparison response model structs

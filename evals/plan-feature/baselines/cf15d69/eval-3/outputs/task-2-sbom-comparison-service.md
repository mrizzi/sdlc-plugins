## Repository
trustify-backend

## Target Branch
main

## Description
Implement the SBOM comparison service logic that computes an on-the-fly diff between two SBOMs. This method queries existing package, advisory, and license data for both SBOMs and computes the structured diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes). Per the non-functional requirements, no new database tables are needed — the diff is computed from existing relations.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add a `pub async fn compare(&self, left_id: Uuid, right_id: Uuid, db: &DatabaseConnection) -> Result<SbomComparisonResult, AppError>` method to `SbomService`

## API Changes
- No endpoint changes in this task (service only)

## Implementation Notes
Add the `compare` method to the existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`. Follow the same error handling pattern used by existing methods (return `Result<T, AppError>` with `.context()` wrapping from `anyhow`).

The method should:
1. Validate that both SBOM IDs exist; return 404 `AppError` if either is missing
2. Fetch packages for both SBOMs using the `sbom_package` entity join (from `entity/src/sbom_package.rs`)
3. Compute added packages (in right but not left) and removed packages (in left but not right)
4. Compute version changes by matching packages by name and comparing versions; determine direction (upgrade/downgrade) using semver comparison
5. Fetch advisories for both SBOMs using the `sbom_advisory` entity join (from `entity/src/sbom_advisory.rs`)
6. Compute new vulnerabilities (advisories in right but not left) and resolved vulnerabilities (in left but not right)
7. Compute license changes by comparing the `license` field from `PackageSummary` (see `modules/fundamental/src/package/model/summary.rs`) for packages present in both SBOMs
8. Assemble and return `SbomComparisonResult`

Use the query helpers from `common/src/db/query.rs` for any filtering logic. Reference the `PackageSummary` struct (which includes a `license` field) from `modules/fundamental/src/package/model/summary.rs` and the `AdvisorySummary` struct (which includes a `severity` field) from `modules/fundamental/src/advisory/model/summary.rs`.

Per Key Conventions (Error handling): Return `Result<T, AppError>` with `.context()` wrapping on all fallible operations. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's handler/service scope.

Per Key Conventions (Module pattern): Place service logic under `service/` within the `sbom` module. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service directory scope.

## Acceptance Criteria
- [ ] `SbomService::compare` method is implemented and returns `SbomComparisonResult`
- [ ] Method returns 404 error when either SBOM ID does not exist
- [ ] Added and removed packages are correctly computed
- [ ] Version changes include direction (upgrade/downgrade)
- [ ] New and resolved vulnerabilities are correctly computed using advisory data
- [ ] License changes are correctly computed for packages present in both SBOMs
- [ ] Performance target: handles SBOMs with up to 2000 packages each efficiently (single query per data type, no N+1)

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package sets, verify added/removed packages
- [ ] Unit test: verify version change direction detection (upgrade vs downgrade)
- [ ] Unit test: verify new/resolved vulnerability detection
- [ ] Unit test: verify license change detection
- [ ] Unit test: verify 404 error when SBOM ID does not exist

## Dependencies
- Depends on: Task 1 — SBOM comparison model types

[sdlc-workflow] Description digest: sha256-md:9ec959cb56c34e8453795e0f8daa870cee7672c64033848279d5baf673846ee5

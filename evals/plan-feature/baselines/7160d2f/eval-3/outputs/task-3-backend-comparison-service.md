## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comparison logic to the SbomService that computes a structured diff between two SBOMs. The service loads both SBOMs' package lists, advisory associations, and license data, then computes set differences for each diff category. This is the core business logic for the SBOM comparison feature, consumed by the endpoint in Task 4.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — export any new helper types if needed

## Implementation Notes
Add a `compare(&self, left_id: Uuid, right_id: Uuid) -> Result<SbomComparison, AppError>` method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`.

Follow the existing service method patterns in the same file (e.g., `fetch`, `list`, `ingest`). Each method uses `.context()` wrapping for error propagation and returns `Result<T, AppError>`.

The comparison logic should:
1. Fetch both SBOMs by ID (reuse existing `fetch` method)
2. Load packages for both SBOMs using `PackageService` from `modules/fundamental/src/package/service/mod.rs`
3. Load advisory associations for both SBOMs using `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs`
4. Compute set differences:
   - Added packages: packages in right not in left (by package name)
   - Removed packages: packages in left not in right
   - Version changes: packages in both but with different versions, determine direction (upgrade/downgrade by semver comparison)
   - New vulnerabilities: advisories affecting right SBOM packages not affecting left
   - Resolved vulnerabilities: advisories affecting left SBOM packages not affecting right
   - License changes: packages in both with different license values
5. Return `SbomComparison` struct from Task 2

No new database tables are required — compute diff on-the-fly from existing package and advisory data per the non-functional requirements.

Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use HashMaps for O(1) lookups during set difference computation rather than nested iteration.

Use query helpers from `common/src/db/query.rs` for any database queries needed to load package/advisory data.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods to reuse for loading SBOMs
- `modules/fundamental/src/package/service/mod.rs::PackageService` — service for loading packages associated with an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — service for loading advisories associated with SBOM packages
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type for Result wrapping

## Acceptance Criteria
- [ ] `SbomService::compare` method computes all six diff categories correctly
- [ ] Added/removed packages are correctly identified by set difference on package names
- [ ] Version changes correctly detect upgrade vs downgrade direction
- [ ] New/resolved vulnerabilities are correctly identified by advisory association differences
- [ ] License changes are correctly identified for packages present in both SBOMs
- [ ] Method returns appropriate error for non-existent SBOM IDs
- [ ] Performance is acceptable for SBOMs with up to 2000 packages (uses HashMap-based lookups)

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences — verify added/removed packages
- [ ] Unit test: compare two SBOMs with version changes — verify upgrade/downgrade detection
- [ ] Unit test: compare two SBOMs with different advisory associations — verify new/resolved vulnerabilities
- [ ] Unit test: compare two SBOMs with license changes — verify license diff
- [ ] Unit test: compare identical SBOMs — all diff categories should be empty
- [ ] Unit test: compare with non-existent SBOM ID — verify error handling

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 2 — Add SBOM comparison response model types

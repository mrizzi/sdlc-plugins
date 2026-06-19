## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison domain model and diff computation service. This task creates the data structures for the structured diff response and implements the logic to compare two SBOMs by loading their packages and advisories, then computing added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` with a `compare(left_id, right_id, db)` method that loads packages and advisories for both SBOMs and computes the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new service module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — derive `Serialize`, `Deserialize`, `Clone`, `Debug` on all structs.
- Use `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` as the reference for package fields (name, version, license).
- Use `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` as the reference for advisory fields (advisory_id, severity, title).
- Load packages for each SBOM via `PackageService` in `modules/fundamental/src/package/service/mod.rs`, filtering by SBOM ID.
- Load advisories for each SBOM via `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`, filtering by SBOM ID.
- Compute diffs using set operations on package names: added = right - left, removed = left - right, version_changes = intersection where version differs.
- For vulnerability diff, compare advisory sets between the two SBOMs.
- For license changes, compare license fields of packages present in both SBOMs.
- The diff MUST be computed on-the-fly (no new database tables per the non-functional requirements).
- Return `Result<SbomComparison, AppError>` following the error handling pattern in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch SBOM details by ID to validate both SBOMs exist before comparing
- `modules/fundamental/src/package/service/mod.rs::PackageService` — list packages filtered by SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — list advisories filtered by SBOM
- `common/src/error.rs::AppError` — error type with `.context()` wrapping pattern

## Acceptance Criteria
- [ ] `SbomComparison` struct contains fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] `compare()` method correctly identifies packages added in the right SBOM but absent in the left
- [ ] `compare()` method correctly identifies packages removed (present in left, absent in right)
- [ ] `compare()` method detects version changes for packages present in both SBOMs
- [ ] `compare()` method detects new vulnerabilities (advisories in right SBOM not in left)
- [ ] `compare()` method detects resolved vulnerabilities (advisories in left SBOM not in right)
- [ ] `compare()` method detects license changes for packages present in both SBOMs
- [ ] Returns `AppError` when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package sets and verify all diff categories are correctly populated
- [ ] Unit test: compare identical SBOMs and verify all diff categories are empty
- [ ] Unit test: compare with a non-existent SBOM ID and verify error is returned
- [ ] Unit test: verify `direction` field in `VersionChange` correctly reports "upgrade" vs "downgrade"

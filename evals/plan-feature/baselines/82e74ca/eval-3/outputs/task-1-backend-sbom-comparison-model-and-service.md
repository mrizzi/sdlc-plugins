# Task 1 — Backend SBOM comparison diff model and service

## Repository
trustify-backend

## Description
Add the data model structs and service logic for computing a structured diff between two SBOMs. This is the core domain logic that compares the package lists, vulnerability advisories, and license mappings of two SBOM versions and returns a structured result containing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing data — no new database tables are required.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new comparison model module
- `modules/fundamental/src/sbom/service/mod.rs` — re-export the new comparison service module

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs
- `modules/fundamental/src/sbom/service/compare.rs` — implement `SbomService::compare(left_id, right_id)` method that computes the diff

## API Changes
- `SbomService::compare(left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` — NEW: service method that loads both SBOMs' packages/advisories/licenses and computes the structured diff

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: models in `model/`, service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive Serialize, Deserialize, Clone, Debug).
- The service method should use the existing `SbomService` (in `modules/fundamental/src/sbom/service/sbom.rs`) to fetch SBOM details and package lists for both left and right SBOMs.
- Use the existing `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) to retrieve package details including license information via the `package_license` entity.
- Use the existing `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`) to fetch advisories linked to each SBOM via the `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`).
- Compute the diff by building HashMaps keyed on package name, then comparing presence and version between left and right sets. For vulnerabilities, compare advisory sets linked to each SBOM. For licenses, compare the license field on packages present in both SBOMs.
- Error handling: use `Result<T, AppError>` with `.context()` wrapping, consistent with `common/src/error.rs`.
- The comparison must meet the p95 < 1s performance requirement for SBOMs with up to 2000 packages each — avoid N+1 queries by batch-loading packages and advisories for each SBOM in bulk.
- The `direction` field on `VersionChange` should be "upgrade" or "downgrade", determined by semver comparison where possible, falling back to string comparison.
- Per the non-functional requirements: no new database tables — compute everything from existing `sbom`, `package`, `sbom_package`, `advisory`, `sbom_advisory`, and `package_license` entities.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for loading SBOM data; extend rather than duplicate
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for loading advisory data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for loading package data
- `entity/src/sbom_package.rs` — existing join table entity for SBOM-Package relationships
- `entity/src/sbom_advisory.rs` — existing join table entity for SBOM-Advisory relationships
- `entity/src/package_license.rs` — existing entity for package license mappings
- `common/src/error.rs::AppError` — existing error type for consistent error handling
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Each sub-struct matches the response shape specified in the feature requirements (e.g., `AddedPackage` has `name`, `version`, `license`, `advisory_count` fields)
- [ ] `SbomService::compare()` correctly identifies packages present in the right SBOM but not in the left as "added"
- [ ] `SbomService::compare()` correctly identifies packages present in the left SBOM but not in the right as "removed"
- [ ] `SbomService::compare()` correctly identifies packages present in both with different versions as "version changes" with correct upgrade/downgrade direction
- [ ] `SbomService::compare()` correctly identifies advisories affecting the right SBOM but not the left as "new vulnerabilities"
- [ ] `SbomService::compare()` correctly identifies advisories affecting the left SBOM but not the right as "resolved vulnerabilities"
- [ ] `SbomService::compare()` correctly identifies packages whose license changed between the two SBOMs
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test: comparing two SBOMs where the right has additional packages produces correct `added_packages`
- [ ] Unit test: comparing two SBOMs where the left has packages not in the right produces correct `removed_packages`
- [ ] Unit test: comparing two SBOMs with the same package at different versions produces correct `version_changes` with direction
- [ ] Unit test: comparing two SBOMs with different advisory associations produces correct `new_vulnerabilities` and `resolved_vulnerabilities`
- [ ] Unit test: comparing two SBOMs where a package's license changed produces correct `license_changes`
- [ ] Unit test: comparing two identical SBOMs returns empty diff (all arrays empty)
- [ ] Unit test: comparing SBOMs with no packages returns empty diff without errors

## Dependencies
- None (this is the foundation task)

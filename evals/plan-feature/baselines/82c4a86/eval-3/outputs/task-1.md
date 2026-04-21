# Task 1 — Add SBOM comparison model and diff service

## Repository
trustify-backend

## Description
Create the data model for SBOM comparison results and implement the diff computation logic in SbomService. The service method accepts two SBOM IDs, loads their package lists, advisory associations, and license data, then computes the structured diff: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This is computed on-the-fly from existing data — no new database tables.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new comparison model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange structs

## API Changes
- None (this task adds service logic only; the endpoint is Task 2)

## Implementation Notes
- Follow the existing module pattern: model structs in `model/`, service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` for the struct pattern (derive Serialize, Deserialize, Clone, Debug).
- The `compare` method on SbomService should accept two SBOM IDs (UUIDs), load both SBOMs using the existing `fetch` method, then load their associated packages via PackageService and advisories via AdvisoryService.
- Diff logic: compute set differences on package names to find added/removed; compare versions for shared packages; compare advisory sets to find new/resolved vulnerabilities; compare license fields for license changes.
- Use `PackageSummary` (from `modules/fundamental/src/package/model/summary.rs`) which includes the `license` field for license comparison.
- Use `AdvisorySummary` (from `modules/fundamental/src/advisory/model/summary.rs`) which includes the `severity` field for vulnerability classification.
- Return `AppError` (from `common/src/error.rs`) with `.context()` wrapping for error cases (SBOM not found, database errors).
- Per constraints (1.1-1.3): this is a planning output only — implementation follows via implement-task.
- Per constraints (5.4): reuse existing SbomService::fetch, PackageService, and AdvisoryService rather than writing new query logic.
- Non-functional: must handle SBOMs with up to 2000 packages each within p95 < 1s. Consider loading packages in batch rather than individually.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods to load SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch packages associated with an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories for vulnerability comparison
- `common/src/error.rs::AppError` — standard error type with IntoResponse implementation
- `entity/src/sbom_package.rs` — SBOM-Package join entity for loading package associations
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for loading advisory associations
- `entity/src/package_license.rs` — Package-License mapping entity for license data

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] `SbomService::compare(left_id, right_id)` returns `Result<SbomComparisonResult, AppError>`
- [ ] Added packages are those in right SBOM but not in left
- [ ] Removed packages are those in left SBOM but not in right
- [ ] Version changes list packages present in both with different versions, indicating upgrade/downgrade direction
- [ ] New vulnerabilities are advisories affecting the right SBOM but not the left
- [ ] Resolved vulnerabilities are advisories affecting the left SBOM but not the right
- [ ] License changes list packages present in both with different license values
- [ ] Comparing an SBOM with itself returns empty diff lists
- [ ] Requesting a non-existent SBOM ID returns an appropriate error

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences, verify added/removed/changed counts
- [ ] Unit test: compare identical SBOMs, verify all diff lists are empty
- [ ] Unit test: compare SBOMs where one has advisories the other does not, verify new/resolved vulnerability lists
- [ ] Unit test: compare SBOMs with license changes on shared packages
- [ ] Unit test: compare with a non-existent SBOM ID, verify error returned

## Verification Commands
- `cargo test --package fundamental -- sbom::service::test_compare` — all comparison service tests pass
- `cargo check --package fundamental` — no compilation errors

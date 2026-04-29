# Task 1 — Backend comparison model and service

## Repository
trustify-backend

## Description
Add the data model structs and service method for SBOM comparison. This task introduces the diff computation logic that compares two SBOMs by their packages, vulnerabilities, and licenses, producing a structured result. The diff is computed on-the-fly from existing entity data — no new database tables are required.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new comparison model types
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` structs

## API Changes
- `SbomService::compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` — NEW: computes structured diff between two SBOMs

## Implementation Notes
- Follow the existing model pattern: each domain entity has a dedicated file in `model/` (see `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for examples).
- The `SbomComparisonResult` struct should be serializable (derive `Serialize`) and contain:
  - `added_packages: Vec<PackageDiff>` — packages in right SBOM but not in left
  - `removed_packages: Vec<PackageDiff>` — packages in left SBOM but not in right
  - `version_changes: Vec<VersionChange>` — packages in both but with different versions, including `direction` field ("upgrade" or "downgrade")
  - `new_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting right SBOM but not left
  - `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — advisories affecting left SBOM but not right
  - `license_changes: Vec<LicenseChange>` — packages whose license changed between the two SBOMs
- The `compare` method in `SbomService` should:
  1. Load both SBOMs by ID using the existing `fetch` method
  2. Load packages for each SBOM using `PackageService` (see `modules/fundamental/src/package/service/mod.rs`)
  3. Load advisories for each SBOM using `AdvisoryService` (see `modules/fundamental/src/advisory/service/advisory.rs`)
  4. Compute set differences for packages (by name), advisories, and licenses
  5. Determine version change direction by comparing version strings
- Use the existing `AppError` enum from `common/src/error.rs` for error handling with `.context()` wrapping.
- The `PackageSummary` struct (in `modules/fundamental/src/package/model/summary.rs`) includes a `license` field — use this for license change detection.
- The `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`) includes a `severity` field — include severity in `VulnerabilityDiff`.
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Consider using `HashSet` or `HashMap` for O(1) lookups during diff computation rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with `fetch` and `list` methods; extend with `compare`
- `modules/fundamental/src/package/service/mod.rs::PackageService` — load packages associated with an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — load advisories associated with an SBOM
- `common/src/error.rs::AppError` — standard error type for service methods
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct pattern and serialization derives
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains `license` field needed for license diff

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and sub-types are defined in `modules/fundamental/src/sbom/model/comparison.rs`
- [ ] `SbomService::compare` method computes correct diffs for added/removed packages, version changes, new/resolved vulnerabilities, and license changes
- [ ] Version change direction is correctly classified as "upgrade" or "downgrade"
- [ ] Diff computation uses efficient data structures (HashMap/HashSet) for O(n) performance
- [ ] All structs derive `Serialize` for JSON response serialization
- [ ] Error cases (SBOM not found) return appropriate `AppError` variants

## Test Requirements
- [ ] Unit test: compare two SBOMs with added and removed packages produces correct `added_packages` and `removed_packages`
- [ ] Unit test: compare two SBOMs with same package at different versions produces correct `version_changes` with direction
- [ ] Unit test: compare two SBOMs where right SBOM has new advisory produces correct `new_vulnerabilities`
- [ ] Unit test: compare two SBOMs where left SBOM advisory is absent in right produces correct `resolved_vulnerabilities`
- [ ] Unit test: compare two SBOMs where a package license changed produces correct `license_changes`
- [ ] Unit test: compare with non-existent SBOM ID returns appropriate error

## Dependencies
- None (this is the foundational task)

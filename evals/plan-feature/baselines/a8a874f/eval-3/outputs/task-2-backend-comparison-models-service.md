# TC-9003-2: Backend comparison models and diff service

## Repository

trustify-backend

## Target Branch

TC-9003

## Description

Define the comparison response models and implement the core diff service that computes the structured difference between two SBOMs. The service compares package lists, advisory associations, and license information to produce categorized diff results (added/removed packages, version changes, new/resolved vulnerabilities, license changes). This is computed on-the-fly from existing entity data without new database tables, per the NFR constraints.

## Files to Create

- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison response structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `modules/fundamental/src/sbom/service/comparison.rs` — `SbomComparisonService` with `compare(left_id, right_id)` method

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the new service module

## Implementation Notes

- Follow the existing module pattern in `modules/fundamental/src/sbom/`: model structs in `model/`, service logic in `service/`.
- The `SbomComparison` struct should include fields matching the API response shape: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`.
- The `SbomComparisonService::compare` method should:
  1. Use `SbomService` (in `modules/fundamental/src/sbom/service/sbom.rs`) to load both SBOMs and their package lists.
  2. Use `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) to retrieve package details including license information.
  3. Use `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`) to fetch advisories linked to each SBOM via the `sbom_advisory` join entity.
  4. Compute set differences for packages (by package name), version comparisons, vulnerability diffs, and license diffs.
- All service methods should return `Result<T, AppError>` consistent with `common/src/error.rs`.
- The `PackageDiff` struct should include `name`, `version`, `license`, and `advisory_count` fields to match the Figma-specified table columns.
- The `VulnerabilityDiff` struct should include `advisory_id`, `severity`, `title`, and `affected_package` fields.
- Derive `Serialize` on all model structs for JSON response serialization.

## Acceptance Criteria

- [ ] `SbomComparison` struct serializes to the JSON shape specified in the feature requirements
- [ ] `SbomComparisonService::compare` correctly identifies added, removed, and version-changed packages
- [ ] Vulnerability diffs correctly distinguish new vs. resolved advisories
- [ ] License changes are detected when a package exists in both SBOMs with different license values
- [ ] Service returns `AppError` for invalid SBOM IDs

## Test Requirements

- [ ] Unit tests for `SbomComparisonService::compare` covering: identical SBOMs (empty diff), completely disjoint SBOMs, overlapping packages with version changes, advisory differences, license changes
- [ ] Test that invalid SBOM IDs return appropriate error responses

## Reuse Candidates

- `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` for loading SBOM data
- `PackageService` in `modules/fundamental/src/package/service/mod.rs` for package details
- `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` for advisory lookups
- `AppError` in `common/src/error.rs` for error handling

## Convention Compliance

- `Applies: task creates modules/fundamental/src/sbom/model/comparison.rs and modules/fundamental/src/sbom/service/comparison.rs matching the convention's module pattern (model/ + service/ + endpoints/ structure).`
- `Applies: task creates new service returning Result<T, AppError> matching the convention's error handling scope.`

[Description digest: sha256-md:b4e8d2f1a7c3e9b5d0f6a2c8e4b0d7f3a9c5e1b8d4f0a6c2e8b5d1f7a3c9e5b2]

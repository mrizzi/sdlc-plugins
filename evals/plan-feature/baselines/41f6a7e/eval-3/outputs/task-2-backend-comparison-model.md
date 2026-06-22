# Task 2 — Add SBOM comparison diff model and service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the domain model structs and service logic for computing a structured diff between two SBOMs. The comparison is computed on-the-fly from existing package and advisory data — no new database tables are required. The service fetches both SBOMs' package lists and associated advisories, then computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — structs for the comparison result (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange)
- `modules/fundamental/src/sbom/service/comparison.rs` — SbomComparisonService with the diff computation logic

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod comparison;` to expose the new service module

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: model structs in `model/`, service logic in `service/`.
- Reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` for package identity and license data.
- Reuse `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` for vulnerability/severity data.
- Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch SBOM details and their associated packages.
- Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to list packages for each SBOM.
- Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to find advisories associated with each SBOM's packages.
- The diff algorithm should:
  1. Fetch the package list for both SBOMs using the existing sbom-package join table (`entity/src/sbom_package.rs`)
  2. Compute set differences (added/removed) based on package name
  3. Compute version changes for packages present in both SBOMs with different versions
  4. Fetch advisories for both package sets using the sbom-advisory join table (`entity/src/sbom_advisory.rs`)
  5. Compute new/resolved vulnerabilities based on advisory presence
  6. Compute license changes using the package-license mapping (`entity/src/package_license.rs`)
- The direction field in version changes (upgrade/downgrade) should use semantic version comparison where possible.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling pattern in `common/src/error.rs`.
- Performance target: p95 < 1s for SBOMs with up to 2000 packages each. Consider using HashSets for O(1) lookups during diff computation.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM details and related data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for listing packages
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for fetching advisories
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license data

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] `PackageDiff` struct contains: `name`, `version`, `license`, `advisory_count`
- [ ] `VersionChange` struct contains: `name`, `left_version`, `right_version`, `direction`
- [ ] `VulnerabilityDiff` struct contains: `advisory_id`, `severity`, `title`, `affected_package`
- [ ] `LicenseChange` struct contains: `name`, `left_license`, `right_license`
- [ ] Comparison service correctly identifies added packages (in right but not left)
- [ ] Comparison service correctly identifies removed packages (in left but not right)
- [ ] Comparison service correctly identifies version changes for packages in both SBOMs
- [ ] Comparison service correctly identifies new and resolved vulnerabilities
- [ ] Comparison service correctly identifies license changes
- [ ] All structs derive `Serialize` for JSON response serialization

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with added packages returns correct `added_packages` list
- [ ] Unit test: comparison of two SBOMs with removed packages returns correct `removed_packages` list
- [ ] Unit test: comparison of two SBOMs with version changes returns correct `version_changes` with upgrade/downgrade direction
- [ ] Unit test: comparison of two SBOMs with new vulnerabilities returns correct `new_vulnerabilities` list
- [ ] Unit test: comparison of two SBOMs with resolved vulnerabilities returns correct `resolved_vulnerabilities` list
- [ ] Unit test: comparison of two SBOMs with license changes returns correct `license_changes` list
- [ ] Unit test: comparison of two identical SBOMs returns all empty diff categories

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

# Task 1 — Add SBOM comparison diff model and service logic

## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model structs and service method for computing a structured diff between two SBOMs. The comparison is computed on-the-fly from existing package, advisory, and license data — no new database tables are required. The service method accepts two SBOM IDs, loads their package lists with associated advisories and licenses, and returns a structured diff result containing added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the SBOM comparison result: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison model module
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare` method to `SbomService` that computes the diff between two SBOMs

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definition conventions (derive `Serialize`, `Deserialize`, `Clone`, `Debug`).
- The `compare` method on `SbomService` should:
  1. Load both SBOMs by ID using the existing `fetch` method in `modules/fundamental/src/sbom/service/sbom.rs`
  2. Load packages for each SBOM using `PackageService` from `modules/fundamental/src/package/service/mod.rs`
  3. Load advisories for each SBOM using `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs`
  4. Compute set differences for packages (by package name), version changes (same name, different version), vulnerability diffs (by advisory ID), and license changes (same package, different license)
- Use the existing `PackageSummary` struct (in `modules/fundamental/src/package/model/summary.rs`) which includes the `license` field for license comparison.
- Use the existing `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`) which includes the `severity` field for vulnerability categorization.
- Return `Result<SbomComparisonResult, AppError>` following the error handling pattern in `common/src/error.rs` with `.context()` wrapping on fallible operations.
- The comparison must perform well for SBOMs with up to 2000 packages each (p95 < 1s). Use `HashMap`-based lookups for O(n) diffing instead of nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with `fetch` and `list` methods; add the `compare` method here
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use to load packages for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use to load advisories associated with each SBOM
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse for package name, version, and license fields
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reuse for advisory ID, severity, and title fields
- `common/src/error.rs::AppError` — reuse for error handling pattern

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct exists with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Each sub-struct contains the fields specified in the API response shape (see feature description)
- [ ] `SbomService::compare(left_id, right_id)` method returns a correct diff for two valid SBOM IDs
- [ ] Method returns `AppError` with appropriate context when either SBOM ID does not exist
- [ ] Diff computation uses HashMap-based lookups for O(n) performance

## Test Requirements
- [ ] Unit test: `compare` returns empty diff when both SBOMs have identical packages
- [ ] Unit test: `compare` correctly identifies added packages (present in right, absent in left)
- [ ] Unit test: `compare` correctly identifies removed packages (present in left, absent in right)
- [ ] Unit test: `compare` correctly identifies version changes for same-named packages
- [ ] Unit test: `compare` correctly identifies new vulnerabilities (advisories in right SBOM not in left)
- [ ] Unit test: `compare` correctly identifies resolved vulnerabilities (advisories in left SBOM not in right)
- [ ] Unit test: `compare` correctly identifies license changes for same-named packages
- [ ] Unit test: `compare` returns error when SBOM ID does not exist

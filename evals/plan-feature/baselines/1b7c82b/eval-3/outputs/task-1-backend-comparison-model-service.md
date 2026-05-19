## Repository
trustify-backend

## Target Branch
main

## Description
Create the data model structs and service logic for SBOM comparison. This task adds the response types that represent a structured diff between two SBOMs and implements the comparison algorithm in `SbomService`. The diff is computed on-the-fly from existing package, advisory, and license data -- no new database tables are required.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Structs for the comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `VulnerabilityDiff`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` to expose the new module
- `modules/fundamental/src/sbom/service/sbom.rs` -- Add a `compare(left_id, right_id) -> Result<SbomComparison, AppError>` method to `SbomService`

## API Changes
- None (this task adds the service layer only; the endpoint is Task 2)

## Implementation Notes
- Define all comparison structs with `#[derive(Serialize, Deserialize, Debug, Clone)]` following the pattern used by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`.
- The `SbomComparison` struct fields should match the API response shape from the Figma design context: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- The `compare` method on `SbomService` should:
  1. Fetch both SBOMs using the existing `SbomService::fetch()` method in `modules/fundamental/src/sbom/service/sbom.rs`.
  2. Load packages for each SBOM via `PackageService` in `modules/fundamental/src/package/service/mod.rs`, using the SBOM-Package join from `entity/src/sbom_package.rs`.
  3. Compute set differences for added/removed packages (present in one but not the other by package name).
  4. Compute version changes for packages present in both SBOMs but with differing versions, including a `direction` field ("upgrade" or "downgrade") using semver comparison.
  5. Load advisories for each SBOM via `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`, using the SBOM-Advisory join from `entity/src/sbom_advisory.rs`.
  6. Compute new vulnerabilities (advisories affecting right but not left) and resolved vulnerabilities (advisories affecting left but not right).
  7. Compute license changes for packages present in both SBOMs but with different license values, using the license field from `PackageSummary` in `modules/fundamental/src/package/model/summary.rs`.
- Use `AppError` from `common/src/error.rs` for error handling, wrapping with `.context()` as done in existing service methods.
- Performance: for SBOMs with up to 2000 packages, use `HashMap` keyed by package name for O(n) diff computation.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Reuse `fetch()` to load SBOM details by ID
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Reuse `list()` or equivalent to load packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- Reuse to load advisories associated with each SBOM
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- Provides `license` field needed for license change detection
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Provides `severity` field needed for vulnerability diff entries
- `common/src/error.rs::AppError` -- Standard error type for service methods

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields matching the expected API response shape
- [ ] `SbomService::compare()` correctly identifies added and removed packages between two SBOMs
- [ ] `SbomService::compare()` correctly identifies version changes with upgrade/downgrade direction
- [ ] `SbomService::compare()` correctly identifies new and resolved vulnerabilities
- [ ] `SbomService::compare()` correctly identifies license changes
- [ ] Returns `AppError` with appropriate status when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff lists
- [ ] Unit test: SBOM with added packages shows them in `added_packages`
- [ ] Unit test: SBOM with removed packages shows them in `removed_packages`
- [ ] Unit test: package version upgrade is classified with direction "upgrade"
- [ ] Unit test: package version downgrade is classified with direction "downgrade"
- [ ] Unit test: new advisory in right SBOM appears in `new_vulnerabilities`
- [ ] Unit test: advisory resolved in right SBOM appears in `resolved_vulnerabilities`
- [ ] Unit test: license change between SBOMs appears in `license_changes`
- [ ] Unit test: nonexistent SBOM ID returns an error

## Verification Commands
- `cargo test --package fundamental -- sbom::service::compare` -- All comparison service tests pass
- `cargo check --package fundamental` -- No compilation errors

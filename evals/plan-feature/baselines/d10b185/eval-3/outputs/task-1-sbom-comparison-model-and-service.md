# Task 1 — Add SBOM comparison model and diff service

## Repository
trustify-backend

## Target Branch
main

## Description
Create the data model and service logic for computing a structured diff between two SBOMs. The comparison service fetches both SBOMs' package sets, advisory associations, and license mappings, then computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This task provides the core business logic that the comparison endpoint (Task 2) will expose via REST.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Defines the `SbomComparison` response struct and its sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`)
- `modules/fundamental/src/sbom/service/comparison.rs` — Implements the `compare` method on `SbomService` that loads two SBOMs' package and advisory data and computes the structured diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the new service module

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: model structs in `model/`, service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` for the struct definition pattern (derive `Serialize`, `Deserialize`, `Debug`, `Clone`).
- The `SbomComparison` struct must match the API response shape specified in the feature requirements:
  ```
  {
    added_packages: Vec<AddedPackage>,
    removed_packages: Vec<RemovedPackage>,
    version_changes: Vec<VersionChange>,
    new_vulnerabilities: Vec<NewVulnerability>,
    resolved_vulnerabilities: Vec<ResolvedVulnerability>,
    license_changes: Vec<LicenseChange>
  }
  ```
- The comparison service should use `PackageService` to fetch packages for each SBOM, and `AdvisoryService` to fetch advisories linked to each SBOM. Use existing join table entities `sbom_package` and `sbom_advisory` from `entity/src/` to query relationships.
- Compute diffs by collecting each SBOM's packages into HashMaps keyed by package name, then iterating to find added (right-only), removed (left-only), and changed (both present, different version) entries.
- For vulnerability diff: collect advisories linked to each SBOM's packages via `sbom_advisory` entity, then compute set differences.
- For license changes: compare `license` field on `PackageSummary` for packages present in both SBOMs.
- Use `AppError` from `common/src/error.rs` for error handling with `.context()` wrapping.
- The non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages. Use batch queries rather than per-package lookups.
- Per the feature requirements: "No new database tables — compute diff on-the-fly from existing package and advisory data."

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with `fetch` and `list` methods; extend this with the `compare` method
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package data for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisory data linked to packages
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying package associations
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisory associations
- `entity/src/package_license.rs` — Package-License mapping for license comparison
- `common/src/error.rs::AppError` — standard error type for service methods

## Acceptance Criteria
- [ ] `SbomComparison` struct is defined with all six diff category fields matching the API response shape
- [ ] Each sub-struct (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) contains the correct fields per the feature spec
- [ ] `SbomService::compare(left_id, right_id)` correctly computes added, removed, and version-changed packages
- [ ] `SbomService::compare` correctly computes new and resolved vulnerabilities between the two SBOMs
- [ ] `SbomService::compare` correctly computes license changes for packages present in both SBOMs
- [ ] Error handling returns appropriate `AppError` when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: comparing two SBOMs where the right has additional packages produces correct `added_packages`
- [ ] Unit test: comparing two SBOMs where the left has packages not in the right produces correct `removed_packages`
- [ ] Unit test: comparing two SBOMs with the same package at different versions produces correct `version_changes` with upgrade/downgrade direction
- [ ] Unit test: comparing two SBOMs with different advisory associations produces correct `new_vulnerabilities` and `resolved_vulnerabilities`
- [ ] Unit test: comparing two SBOMs where a package changed license produces correct `license_changes`
- [ ] Unit test: comparing identical SBOMs produces empty diff arrays
- [ ] Unit test: comparing with a non-existent SBOM ID returns an error

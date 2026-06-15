## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison domain model and service layer. Define the structs that represent a structured diff between two SBOMs (added/removed packages, version changes, new/resolved vulnerabilities, license changes) and implement the service method that computes this diff by querying existing package, advisory, and license data. No new database tables are needed — the diff is computed on-the-fly from existing data.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the comparison result: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare` method that takes two SBOM IDs and returns `SbomComparisonResult`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new service module

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/` where models are in `model/` and service logic is in `service/`. The comparison structs should derive `Serialize` and `Deserialize` like `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`.

The `compare` service method should:
1. Load packages for both SBOMs using the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`
2. Load advisories for both SBOMs using the existing `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
3. Compute set differences for packages (added/removed), version changes, vulnerability changes, and license changes
4. Return `Result<SbomComparisonResult, AppError>` following the error handling pattern in `common/src/error.rs` using `.context()` wrapping

Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use hash-based lookups (HashMap keyed by package name) for O(n) comparison rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference for struct derivation patterns (Serialize, Deserialize) and field naming conventions
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Reference for detailed model struct patterns
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with fetch and list methods; the compare method extends this service
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Package lookup service to reuse for loading package data per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Advisory lookup service to reuse for vulnerability correlation
- `common/src/error.rs::AppError` — Error type all service methods must return

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains fields for all six diff categories: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Each diff category uses a dedicated struct with the fields specified in the feature requirements
- [ ] `SbomService::compare` method accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] The comparison uses hash-based lookups for O(n) performance
- [ ] All structs derive `Serialize` and `Deserialize`

## Test Requirements
- [ ] Unit test: compare two identical SBOMs returns empty diff in all categories
- [ ] Unit test: compare SBOMs where the right has an additional package returns it in `added_packages`
- [ ] Unit test: compare SBOMs where a package version differs returns it in `version_changes` with correct direction (upgrade/downgrade)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:92e2253f9fc71dc9eaba7f86004717c7bb3865a64790bd1bb7d43f96d349ff2e

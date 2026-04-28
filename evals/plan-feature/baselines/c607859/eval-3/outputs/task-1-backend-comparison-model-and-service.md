# Task 1 -- Backend Comparison Model and Service

## Repository
trustify-backend

## Description
Add a structured comparison response model and a diff computation method to the SbomService. The model captures all six diff categories defined in the feature requirements: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The service method fetches package and advisory data for two SBOMs and computes the diff on-the-fly without new database tables, respecting the p95 < 1s performance requirement for SBOMs with up to 2000 packages each.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- SbomComparisonResult struct and per-category diff structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to SbomService

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct conventions (derive Serialize, Deserialize, Clone, Debug).
- The comparison method should load packages for both SBOMs via the existing PackageService in `modules/fundamental/src/package/service/mod.rs`, and advisories via AdvisoryService in `modules/fundamental/src/advisory/service/advisory.rs`.
- Use the `sbom_package` join table entity (`entity/src/sbom_package.rs`) to resolve which packages belong to each SBOM.
- Use the `sbom_advisory` join table entity (`entity/src/sbom_advisory.rs`) to resolve which advisories affect each SBOM.
- Use the `package_license` entity (`entity/src/package_license.rs`) to detect license changes.
- Compute the diff in memory using HashMaps keyed by package name for O(n) comparison. No new database tables are needed per the non-functional requirements.
- The `direction` field in VersionChange should be "upgrade" or "downgrade" based on semver comparison.
- All handlers in the codebase return `Result<T, AppError>` with `.context()` wrapping -- follow this pattern. See `common/src/error.rs` for the AppError enum.
- Return an error if either SBOM ID does not exist.

## Reuse Candidates
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- provides package fetching logic; reuse for loading packages per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- provides advisory fetching and search; reuse for loading advisories per SBOM
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for model struct conventions
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for resolving package membership
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity for resolving advisory associations
- `common/src/error.rs::AppError` -- error type to use for all Result returns

## Acceptance Criteria
- [ ] SbomComparisonResult struct contains fields for all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each diff category struct contains the fields specified in the API response shape (see feature requirements)
- [ ] SbomService::compare method computes correct diffs by comparing package sets, advisory sets, and license data between two SBOMs
- [ ] Method returns an appropriate AppError if either SBOM ID is not found
- [ ] Version change direction is correctly computed as "upgrade" or "downgrade"
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test: comparing two SBOMs with known package differences produces correct added/removed/changed results
- [ ] Unit test: comparing two identical SBOMs produces empty diff categories
- [ ] Unit test: comparing SBOMs with differing advisories correctly classifies new vs resolved vulnerabilities
- [ ] Unit test: comparing SBOMs with license changes on the same package produces correct license_changes entries
- [ ] Unit test: requesting a non-existent SBOM ID returns an error

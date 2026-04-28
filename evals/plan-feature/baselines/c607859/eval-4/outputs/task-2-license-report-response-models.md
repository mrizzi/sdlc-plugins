# Task 2 -- License Report Response Models

## Repository
trustify-backend

## Description
Create the response model structs for the license compliance report. The report groups all packages in an SBOM by their license type and includes a compliance flag per group based on the license policy. These models will be returned by the license report endpoint and consumed by compliance teams and CI/CD pipelines.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- `LicenseReportGroup` and `LicenseReport` structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` (see `summary.rs` and `details.rs` for struct conventions)
- `LicenseReportGroup` should contain:
  - `license: String` -- the SPDX license identifier
  - `packages: Vec<PackageRef>` -- list of packages with this license (include package name and version)
  - `compliant: bool` -- whether this license group is compliant with the configured policy
- `LicenseReport` should contain:
  - `sbom_id: String` -- the SBOM identifier
  - `groups: Vec<LicenseReportGroup>` -- license groups
  - `compliant: bool` -- overall compliance flag (true only if all groups are compliant)
- Derive `serde::Serialize` for API response serialization, matching the existing model patterns
- The `PackageRef` inner struct (or use an existing type if one fits) should include at minimum `name: String` and `version: String`
- Per constraints doc section 5.4: check if `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` can be reused or if a lighter struct is more appropriate

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference pattern for model struct layout and derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` -- reference pattern for nested response structures
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- existing package model that includes the `license` field; evaluate whether to reuse directly or extract a lightweight subset

## Acceptance Criteria
- [ ] `LicenseReport` serializes to JSON matching the expected response shape: `{ sbom_id, groups: [{ license, packages: [...], compliant }], compliant }`
- [ ] `LicenseReportGroup` includes license identifier, package list, and compliance flag
- [ ] Overall `compliant` flag on `LicenseReport` is `false` if any group is non-compliant
- [ ] Model structs follow existing conventions in the `sbom/model/` module

## Test Requirements
- [ ] Unit test: serialize a `LicenseReport` with mixed compliant/non-compliant groups and verify JSON structure
- [ ] Unit test: verify overall `compliant` is `false` when at least one group is non-compliant
- [ ] Unit test: verify overall `compliant` is `true` when all groups are compliant

## Dependencies
- Depends on: Task 1 -- License Policy Configuration Model (for the `is_compliant` method used to set compliance flags)

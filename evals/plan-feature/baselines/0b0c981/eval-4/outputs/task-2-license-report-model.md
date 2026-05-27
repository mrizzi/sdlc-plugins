## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report response model that represents the structured output of the license report endpoint. The model groups packages by license type and includes a compliance flag per group, based on the license policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReportGroup and LicenseReport structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model conventions in `modules/fundamental/src/sbom/model/` (see `summary.rs` and `details.rs` for patterns)
- Define the following structs:
  - `LicenseReportGroup` — represents one license group: `{ license: String, packages: Vec<PackageSummary>, compliant: bool }`
  - `LicenseReport` — the top-level response: `{ groups: Vec<LicenseReportGroup> }`
- Both structs derive `Serialize` for JSON response serialization
- Reference `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` for the package representation within each group (reuse existing type rather than defining a new one)
- Per docs/constraints.md §5.4: do not duplicate the PackageSummary type — import and reuse it

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — sibling model showing the derive and field patterns
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — sibling model for reference
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — the package representation to reuse in license groups (includes the `license` field)

## Acceptance Criteria
- [ ] LicenseReport struct serializes to the expected JSON shape: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] LicenseReportGroup includes license name, list of packages, and compliance flag
- [ ] PackageSummary from the existing package module is reused, not duplicated

## Test Requirements
- [ ] Unit test: serialize a LicenseReport with multiple groups and verify JSON output shape
- [ ] Unit test: verify that compliant flag is correctly represented in serialized output

## Dependencies
- Depends on: Task 1 — License policy model (for the compliance evaluation types)

[sdlc-workflow] Description digest: sha256:f43abcd473315a3da3b6ac2060f0b9be2ec4b7897de8babc1ff1ee825f291bf2

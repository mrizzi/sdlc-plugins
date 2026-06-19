## Repository
trustify-backend

## Target Branch
main

## Description
Define the license compliance report response model structs and the license policy configuration schema. This task establishes the data structures that the service and endpoint layers will use: `LicenseReport` (top-level response), `LicenseGroup` (per-license grouping with compliance flag), and `LicensePolicy` (configurable policy loaded from a JSON file). The policy file defines which licenses are approved, which are denied, and the default stance for unlisted licenses.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReport, LicenseGroup, and PackageLicenseEntry structs with serde Serialize/Deserialize derives
- `license-policy.json` — Default license compliance policy configuration file at the repo root

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct layout and derive macros.
- The `LicenseReport` struct should contain a `Vec<LicenseGroup>` field named `groups`, matching the response shape from the requirements: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.
- Each `LicenseGroup` should have fields: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- `PackageLicenseEntry` should include at minimum: `name: String`, `version: String`, referencing data available from the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` (which includes a `license` field).
- The `LicensePolicy` struct should support: `approved_licenses: Vec<String>`, `denied_licenses: Vec<String>`, `default_policy: String` (one of "allow" or "deny").
- The `license-policy.json` file should contain a sensible default policy with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as approved, and known copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as denied, with `default_policy: "deny"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Pattern for struct definition with serde derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Pattern for nested response structs
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field that maps packages to licenses; useful reference for field naming

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageLicenseEntry` structs are defined with appropriate serde derives
- [ ] `LicensePolicy` struct is defined and can be deserialized from the JSON policy file
- [ ] `license-policy.json` contains a valid default policy with approved and denied license lists
- [ ] `license_report` module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] All structs compile and are accessible from dependent modules

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes correctly from the default `license-policy.json` content
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape `{ groups: [{ license, packages, compliant }] }`

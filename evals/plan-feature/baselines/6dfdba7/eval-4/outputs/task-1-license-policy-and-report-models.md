## Repository
trustify-backend

## Description
Define the license compliance policy configuration format and the response models for the license report endpoint. The policy is a JSON configuration file that lists allowed and denied license identifiers (SPDX IDs). The report models represent the grouped license compliance output returned by the API. This task lays the foundation for the service and endpoint tasks that follow.

## Files to Create
- `license-policy.json` — Default license compliance policy configuration at the repository root. Contains an object with `allowed` and `denied` arrays of SPDX license identifiers, plus a `default_policy` field (`"allow"` or `"deny"`) controlling behavior for unlisted licenses.
- `modules/fundamental/src/sbom/model/license_report.rs` — Rust structs for the license report response: `LicenseReport`, `LicenseGroup`, and `LicensePolicyConfig`.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module.

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each defines a struct with `#[derive(Clone, Debug, Serialize, Deserialize)]` and implements `From` or constructor methods.
- The `LicenseReport` struct should contain:
  - `sbom_id: String` — the SBOM identifier
  - `groups: Vec<LicenseGroup>` — packages grouped by license
  - `total_packages: usize` — total package count
  - `non_compliant_count: usize` — count of non-compliant groups
- The `LicenseGroup` struct should contain:
  - `license: String` — SPDX license identifier
  - `packages: Vec<PackageLicenseEntry>` — list of packages with this license
  - `compliant: bool` — whether this license is policy-compliant
- The `PackageLicenseEntry` struct should contain:
  - `package_name: String`
  - `package_version: String`
  - `transitive: bool` — whether this is a transitive dependency
- The `LicensePolicyConfig` struct should contain:
  - `allowed: Vec<String>` — explicitly allowed SPDX identifiers
  - `denied: Vec<String>` — explicitly denied SPDX identifiers
  - `default_policy: String` — `"allow"` or `"deny"` for unlisted licenses
- Use `serde` for JSON serialization/deserialization, consistent with existing model patterns.
- The `license-policy.json` file should ship with a sensible default: common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed, known copyleft licenses (GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only) as denied, and `default_policy: "deny"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Pattern reference for struct definition with Serialize/Deserialize derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — Pattern reference for nested struct composition
- `entity/src/package_license.rs` — Existing entity defining the package-to-license mapping; the `PackageLicenseEntry` model will be populated from this data

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root with valid JSON containing `allowed`, `denied`, and `default_policy` fields
- [ ] `LicenseReport`, `LicenseGroup`, `PackageLicenseEntry`, and `LicensePolicyConfig` structs are defined with appropriate Serialize/Deserialize derives
- [ ] `LicensePolicyConfig` can be deserialized from `license-policy.json` without errors
- [ ] The model module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Unit test: `LicensePolicyConfig` deserializes correctly from a sample JSON string matching the `license-policy.json` format
- [ ] Unit test: `LicenseReport` serializes to JSON with the expected structure (`groups`, `total_packages`, `non_compliant_count`)
- [ ] Unit test: Default policy file at `license-policy.json` parses without error

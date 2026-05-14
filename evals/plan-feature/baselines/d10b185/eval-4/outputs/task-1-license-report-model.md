# Task 1 — Add license report and policy model structs

## Repository
trustify-backend

## Target Branch
main

## Description
Define the data model structs for the license compliance report feature. This includes the response types for the license report endpoint (`LicenseReport`, `LicenseGroup`, `PackageLicenseInfo`) and the license policy configuration model (`LicensePolicy`). These structs provide the foundation that the service and endpoint layers will build upon.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declarations for new model files

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport`, `LicenseGroup`, and `PackageLicenseInfo` structs with serde serialization
- `modules/fundamental/src/sbom/model/license_policy.rs` — `LicensePolicy` struct with a list of allowed/denied licenses and a method to evaluate compliance

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model file defines a struct with `#[derive(Serialize, Deserialize, Debug, Clone)]`.
- The `LicenseReport` struct should contain:
  - `groups: Vec<LicenseGroup>` — packages grouped by license
  - `total_packages: usize` — total package count
  - `compliant_count: usize` — number of compliant groups
  - `non_compliant_count: usize` — number of non-compliant groups
- The `LicenseGroup` struct should contain:
  - `license: String` — the SPDX license identifier
  - `packages: Vec<PackageLicenseInfo>` — packages with this license
  - `compliant: bool` — whether this license is compliant with policy
- The `PackageLicenseInfo` struct should contain:
  - `name: String` — package name
  - `version: String` — package version
  - `transitive: bool` — whether this is a transitive dependency
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — list of SPDX identifiers considered compliant
  - `denied_licenses: Vec<String>` — list of SPDX identifiers considered non-compliant
  - `default_policy: PolicyDefault` — enum (Allow | Deny) for licenses not in either list
- Use the `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` as reference for the license field pattern — it already includes a `license` field.
- The `package_license` entity in `entity/src/package_license.rs` maps the package-to-license relationship in the database; use this as the data source reference.
- Per constraints doc section 5.3: implementation must follow the patterns referenced in these notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the standard model struct pattern with serde derives
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field pattern to reference
- `entity/src/package_license.rs` — the SeaORM entity mapping packages to licenses; use as the underlying data source

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageLicenseInfo` structs are defined with serde serialization support
- [ ] `LicensePolicy` struct is defined with allowed/denied license lists and a default policy enum
- [ ] `LicensePolicy` has a method `is_compliant(&self, license: &str) -> bool` that evaluates a license against the policy
- [ ] All structs are publicly exported from the sbom model module
- [ ] Code compiles without errors (`cargo build`)

## Test Requirements
- [ ] Unit tests for `LicensePolicy::is_compliant` covering: allowed license returns true, denied license returns false, unknown license with Allow default returns true, unknown license with Deny default returns false
- [ ] Unit tests for serde round-trip serialization of `LicenseReport`

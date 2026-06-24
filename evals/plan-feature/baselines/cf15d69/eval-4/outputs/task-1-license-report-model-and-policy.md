## Repository
trustify-backend

## Target Branch
main

## Description
Define the license compliance report data model and the default license policy configuration. This task introduces the response types for the license report endpoint (`LicenseReport`, `LicenseGroup`) and a JSON-based license policy file that specifies which licenses are allowed or denied.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to re-export the new model module
- `modules/fundamental/Cargo.toml` — Add `serde_json` dependency if not already present (for policy deserialization)

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Defines `LicenseReport`, `LicenseGroup`, and `LicensePolicyConfig` structs with Serialize/Deserialize derives
- `license-policy.json` — Default license compliance policy file listing allowed and denied SPDX license identifiers

## Implementation Notes
- `LicenseReport` should contain a `groups` field: `Vec<LicenseGroup>`.
- `LicenseGroup` should contain: `license: String` (SPDX identifier), `packages: Vec<PackageRef>` (package name and version), `compliant: bool`.
- `PackageRef` is a lightweight struct with `name` and `version` fields, distinct from the full `PackageSummary` in `modules/fundamental/src/sbom/model/../../../package/model/summary.rs`.
- `LicensePolicyConfig` should define `allowed_licenses: Vec<String>` and `denied_licenses: Vec<String>`. When `denied_licenses` is non-empty, any package with a matching license is flagged non-compliant. When `allowed_licenses` is non-empty, only packages with matching licenses are compliant.
- Per Key Conventions (Framework): Use `serde::Serialize` and `serde::Deserialize` derives matching the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`. Applies: task modifies files in `modules/fundamental/src/sbom/model/` matching the convention's module pattern scope.
- Per Key Conventions (Response types): The `LicenseReport` is a single-entity response (not paginated), so it does not need to use `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task creates a new response type in the model layer.

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageRef` structs are defined with `Serialize` and `Deserialize` derives
- [ ] `LicensePolicyConfig` struct is defined and can be deserialized from the `license-policy.json` file
- [ ] `license-policy.json` contains a sensible default policy (e.g., deny GPL-3.0 family, allow MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause)
- [ ] `modules/fundamental/src/sbom/model/mod.rs` re-exports the new module
- [ ] All new structs compile without errors

## Test Requirements
- [ ] Unit test: `LicensePolicyConfig` deserializes correctly from a sample JSON string
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape (`{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`)

[sdlc-workflow] Description digest: sha256-md:9961a3341bcf7d1ae0ede36763e810af35fd7b32e2b1df13c2deea09058c9c68

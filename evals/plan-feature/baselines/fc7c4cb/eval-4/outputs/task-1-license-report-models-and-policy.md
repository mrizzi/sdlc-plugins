## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model types for the license compliance report and the license policy configuration loader. This task defines the response structures (`LicenseGroup`, `LicenseReport`) used by the license report endpoint, and a policy configuration module that loads a JSON policy file specifying allowed and denied license identifiers. The policy configuration enables organizations to define their own compliance rules.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declarations for the new license report model types
- `modules/fundamental/src/sbom/mod.rs` — add module declaration for the new policy submodule (if structured as a sibling to model/service/endpoints)

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseGroup` and `LicenseReport` structs with serde Serialize/Deserialize derives
- `modules/fundamental/src/sbom/policy/mod.rs` — define `LicensePolicy` struct (with `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`) and a `load_policy(path: &Path) -> Result<LicensePolicy>` function
- `license-policy.json` — default license policy configuration file at the repository root with example allowed/denied license lists (MIT, Apache-2.0 as allowed; GPL-3.0 as denied example)

## API Changes
- No API changes in this task (model and configuration only)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) and `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`) for struct definition conventions, derive macros, and field naming.
- The `LicenseReport` struct should contain: `sbom_id`, `groups: Vec<LicenseGroup>`, `policy_violations: usize`, `generated_at: DateTime`.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`. The `PackageLicenseEntry` can reference or reuse fields from `PackageSummary` in `modules/fundamental/src/package/model/summary.rs`.
- The `LicensePolicy` loader should read a JSON file from a configurable path (environment variable or default path). Use `serde_json::from_reader` for deserialization.
- All error types should integrate with `AppError` from `common/src/error.rs` using `.context()` wrapping, following the existing error handling pattern.
- The `compliant` field in `LicenseGroup` is determined by checking whether the license appears in the policy's `denied_licenses` list (non-compliant if present) or is absent from the `allowed_licenses` list when the policy uses an allowlist mode.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct definition patterns (derives, field types, serde attributes)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field; reuse or reference for package license data shape
- `common/src/error.rs::AppError` — error type to integrate with for policy loading errors

## Acceptance Criteria
- [ ] `LicenseGroup` and `LicenseReport` structs are defined with serde Serialize/Deserialize and compile successfully
- [ ] `LicensePolicy` struct and `load_policy` function are implemented and can parse a valid JSON policy file
- [ ] `load_policy` returns a descriptive error (via `AppError`) for missing or malformed policy files
- [ ] A default `license-policy.json` file exists at the repository root with documented example entries
- [ ] All new modules are properly declared in their parent `mod.rs` files

## Test Requirements
- [ ] Unit test: `load_policy` successfully parses a valid policy JSON with both allowed and denied lists
- [ ] Unit test: `load_policy` returns an error for a missing file path
- [ ] Unit test: `load_policy` returns an error for malformed JSON
- [ ] Unit test: verify `LicenseReport` and `LicenseGroup` serialize to the expected JSON shape

## Documentation Updates
- `README.md` — add a section describing the license policy configuration file format and location

[sdlc-workflow] Description digest: sha256:b0197f39900df5dd1f2844d88ca112fb5e1b9e26d2a5005493cbcfb3968c0b26

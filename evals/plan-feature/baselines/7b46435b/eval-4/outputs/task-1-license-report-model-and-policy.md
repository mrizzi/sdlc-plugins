## Repository
trustify-backend

## Target Branch
main

## Description
Create the license compliance report model structs and license policy configuration. This task introduces `LicenseComplianceReport`, `LicenseGroup`, and `PackageLicenseEntry` response structs, along with a `LicensePolicy` struct for loading allowed/denied license lists from a JSON configuration file. The policy configuration enables organizations to define which licenses are compliant with their usage policies.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Major", "fixVersions": "RHTPA 1.5.0" }

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- `LicenseComplianceReport` struct with field `groups: Vec<LicenseGroup>`; `LicenseGroup` struct with fields: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`; `PackageLicenseEntry` struct with fields: `name: String`, `version: String`, `transitive: bool`; `LicensePolicy` struct with fields: `allowed: Vec<String>`, `denied: Vec<String>` for loading policy from JSON config
- `config/license-policy.json` -- default license policy configuration file defining allowed licenses (e.g., MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and denied licenses (e.g., GPL-3.0, AGPL-3.0) as a starting point for customization

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` and re-export `LicenseComplianceReport`, `LicenseGroup`, `PackageLicenseEntry`, `LicensePolicy`

## API Changes
- `LicenseComplianceReport` -- NEW response model: `{ groups: [{ license: "MIT", packages: [{ name: "serde", version: "1.0.0", transitive: false }], compliant: true }] }`

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct layout and derive macros. The new structs should derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`.

The `LicensePolicy` struct should implement a `load(path: &Path) -> Result<LicensePolicy, AppError>` method that reads and deserializes the JSON policy file. Use `serde_json::from_reader` for deserialization. If the file is not found, return a default permissive policy (empty denied list) to allow operation without explicit configuration.

The `LicenseGroup::compliant` flag is determined by checking whether the license name appears in the policy's denied list. If the license is in the denied list, `compliant` is `false`. If an allowed list is non-empty, only licenses in the allowed list are compliant; otherwise all non-denied licenses are compliant.

The `PackageLicenseEntry::transitive` field indicates whether the package is a direct dependency or a transitive (indirect) dependency of the SBOM. This is determined by the dependency graph during report generation (Task 2), but the model must support the field.

Per CONVENTIONS.md: all handlers and service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing model struct demonstrating the derive macro pattern and struct layout to follow
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- another model struct example showing the established pattern
- `entity/src/package_license.rs` -- Package-License mapping entity; defines the license field used in the compliance check
- `common/src/error.rs::AppError` -- standard error type for policy loading errors

## Acceptance Criteria
- [ ] `LicenseComplianceReport` struct exists with `groups: Vec<LicenseGroup>` field
- [ ] `LicenseGroup` struct exists with fields: `license`, `packages`, `compliant`
- [ ] `PackageLicenseEntry` struct exists with fields: `name`, `version`, `transitive`
- [ ] `LicensePolicy` struct exists with fields: `allowed`, `denied` and a `load` method
- [ ] Default license policy JSON file exists at `config/license-policy.json`
- [ ] `LicensePolicy::load` returns a default permissive policy when the config file is missing
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `utoipa::ToSchema`

## Test Requirements
- [ ] Unit test: `LicenseComplianceReport` serializes to expected JSON shape `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test: `LicensePolicy::load` correctly loads and parses a JSON policy file
- [ ] Unit test: `LicensePolicy::load` returns a default permissive policy when the file does not exist
- [ ] Unit test: License compliance check correctly flags denied licenses as non-compliant

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental license_report` -- unit tests pass

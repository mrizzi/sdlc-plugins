# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are not. The policy is loaded from a JSON configuration file in the repository. This provides the foundation for the license compliance report by establishing the rules against which packages are evaluated.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — LicensePolicy struct that deserializes from JSON, containing allowed and denied license lists with a method to check compliance of a given license string
- `license-policy.json` — Default license policy configuration file at the repository root with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and example restricted licenses (GPL-3.0, AGPL-3.0) as denied

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_policy;` to expose the new module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definitions and module organization.
- Use `serde::Deserialize` for JSON deserialization of the policy file, consistent with existing model patterns in the codebase.
- The LicensePolicy struct should include:
  - `allowed_licenses: Vec<String>` — licenses explicitly permitted
  - `denied_licenses: Vec<String>` — licenses explicitly denied
  - A `is_compliant(&self, license: &str) -> bool` method that returns `false` if the license is in the denied list, `true` if in the allowed list, and a configurable default for unknown licenses.
- Per docs/constraints.md §5.3: Follow patterns referenced in the task's Implementation Notes.
- Per docs/constraints.md §5.4: Check for any existing license-related utilities in the codebase before creating new logic.

## Reuse Candidates
- `entity/src/package_license.rs` — Existing package-license mapping entity; understand the license field format to ensure policy matching is compatible with stored license values.
- `common/src/error.rs` — AppError enum for error handling when policy file cannot be loaded or parsed.

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly identifies allowed, denied, and unknown licenses
- [ ] A default license-policy.json exists with sensible defaults
- [ ] Module is properly exported via model/mod.rs

## Test Requirements
- [ ] Unit test: LicensePolicy correctly loads from a JSON string
- [ ] Unit test: `is_compliant` returns true for allowed licenses
- [ ] Unit test: `is_compliant` returns false for denied licenses
- [ ] Unit test: `is_compliant` handles unknown licenses according to default behavior
- [ ] Unit test: Malformed JSON produces a clear error

## Dependencies
- None

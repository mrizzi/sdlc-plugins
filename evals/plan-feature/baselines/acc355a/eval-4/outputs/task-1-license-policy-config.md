# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This provides the foundation for the license compliance report to check packages against.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — License policy struct and deserialization logic
- `license-policy.json` — Default license policy configuration file at repository root

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_policy;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` — see `summary.rs` and `details.rs` for struct conventions (derive macros, serde attributes).
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — list of SPDX license identifiers considered compliant (e.g., "MIT", "Apache-2.0", "BSD-3-Clause")
  - `denied_licenses: Vec<String>` — list of SPDX license identifiers explicitly denied
  - A method to check a given license string against the policy, returning a compliance status
- The default `license-policy.json` should include common permissive licenses as allowed and common copyleft licenses (e.g., "GPL-3.0-only", "AGPL-3.0-only") as denied.
- Use `serde_json` for deserialization, consistent with the rest of the codebase.
- The policy file path should be configurable, with a sensible default pointing to the repository root file.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` which contains the `license` field — the policy will be checked against this field.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field that the policy will validate against
- `common/src/error.rs::AppError` — use for error handling when policy file is missing or malformed

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] Policy provides a method to check if a given license identifier is compliant, denied, or unknown
- [ ] A default `license-policy.json` exists with reasonable defaults for common SPDX licenses
- [ ] The module is properly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON and verify fields
- [ ] Unit test: check a compliant license returns compliant status
- [ ] Unit test: check a denied license returns denied status
- [ ] Unit test: check an unknown license (not in allowed or denied) returns unknown status
- [ ] Unit test: handle malformed JSON gracefully with appropriate error

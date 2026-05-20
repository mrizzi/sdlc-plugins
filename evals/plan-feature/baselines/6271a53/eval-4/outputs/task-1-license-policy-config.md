# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant. The policy is stored as a JSON configuration file in the repository. This provides the foundation for the license compliance report to flag packages with non-compliant licenses.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct with serde deserialization, containing allowed and denied license lists
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` (see `paginated.rs` for struct conventions)
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — licenses considered compliant (e.g., "MIT", "Apache-2.0")
  - `denied_licenses: Vec<String>` — licenses considered non-compliant (e.g., "GPL-3.0")
  - `default_policy: PolicyDefault` — enum of `Allow` or `Deny` for licenses not in either list
- Use `serde::Deserialize` for JSON deserialization, consistent with existing model patterns
- The policy file should be loadable from a configurable path (environment variable or default location)
- Reference the SPDX license identifier format for license string matching
- Per constraints (docs/constraints.md) section 5: code must not duplicate existing functionality — check if any license-related utilities already exist in the codebase

## Reuse Candidates
- `common/src/model/paginated.rs` — demonstrates the struct definition and serde derive pattern used throughout the common module
- `common/src/error.rs` — AppError enum for error handling when policy file is missing or malformed

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON file
- [ ] Default license policy JSON file exists with a reasonable set of common open-source licenses
- [ ] Policy supports allowed list, denied list, and a default disposition for unlisted licenses
- [ ] Invalid or missing policy files produce a clear AppError

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON string into LicensePolicy
- [ ] Unit test: deserialize policy with missing optional fields uses sensible defaults
- [ ] Unit test: invalid JSON returns an appropriate error

## Dependencies
None

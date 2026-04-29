## Repository
trustify-backend

## Description
Add a license policy configuration system that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded by the application at startup. This provides the foundation for the license compliance report feature (TC-9004) by establishing the rules against which packages are evaluated.

## Files to Create
- `common/src/license_policy.rs` — License policy model and loader that reads the JSON config, parses it into a `LicensePolicy` struct, and provides a method to check whether a given license identifier is compliant
- `license-policy.json` — Default license policy configuration file at the repository root, containing lists of allowed and denied SPDX license identifiers

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add `serde_json` dependency if not already present (needed for JSON config parsing)

## Implementation Notes
- Define a `LicensePolicy` struct with fields `allowed: Vec<String>` and `denied: Vec<String>`. A license is compliant if it appears in `allowed` and not in `denied`. If a license appears in neither list, treat it as non-compliant (fail-closed).
- Use `serde::Deserialize` to parse the JSON file, following the same serde patterns used throughout the codebase (e.g., in `entity/src/package.rs` and other entity definitions).
- The policy file path should be configurable via an environment variable (e.g., `LICENSE_POLICY_PATH`) with a default fallback to `license-policy.json` at the repository root.
- Follow the error handling pattern in `common/src/error.rs` — return `AppError` variants for missing or malformed policy files.
- The `LicensePolicy` struct should implement a `fn is_compliant(&self, license: &str) -> bool` method that checks the license identifier against the policy rules.
- The default `license-policy.json` should include common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC) as allowed and common copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as denied, serving as a reasonable starting point.

## Reuse Candidates
- `common/src/error.rs::AppError` — Use the existing error enum for policy loading errors
- `entity/src/package_license.rs` — Reference to understand how license identifiers are stored in the database

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly returns `true` for allowed licenses, `false` for denied or unknown licenses
- [ ] Missing policy file produces a clear `AppError` with descriptive message
- [ ] Malformed JSON in the policy file produces a clear `AppError`
- [ ] Default `license-policy.json` contains reasonable defaults for common SPDX identifiers

## Test Requirements
- [ ] Unit test: `is_compliant` returns `true` for an allowed license
- [ ] Unit test: `is_compliant` returns `false` for a denied license
- [ ] Unit test: `is_compliant` returns `false` for an unknown license not in either list
- [ ] Unit test: Deserializing a valid JSON policy file succeeds
- [ ] Unit test: Deserializing malformed JSON returns an error

## Verification Commands
- `cargo test -p common -- license_policy` — All license policy unit tests pass
- `cargo build -p common` — Common crate builds without errors

## Repository
trustify-backend

## Description
Add a license policy configuration module that defines a `LicensePolicy` struct and loads policy rules from a JSON configuration file. The policy specifies which licenses are allowed (allowlist), which are explicitly denied (denylist), and the default compliance status for unlisted licenses.

## Files to Create
- `common/src/license_policy.rs` — `LicensePolicy` struct with `allowed: Vec<String>`, `denied: Vec<String>`, `default_compliant: bool`; includes `load_from_file(path)` function and `is_compliant(license: &str) -> bool` method

## Files to Modify
- `common/src/lib.rs` — add `pub mod license_policy;` to expose the module

## Implementation Notes
- Follow the existing module pattern in `common/src/` for struct definitions and module exports.
- The `LicensePolicy` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` for JSON deserialization.
- `load_from_file` reads a JSON file from a configurable path and deserializes into `LicensePolicy`.
- `is_compliant` checks: if license is in `denied` → false; if license is in `allowed` → true; otherwise → `default_compliant`.
- Reference `common/src/error.rs::AppError` for error handling when the policy file is missing or malformed.

## Reuse Candidates
- `common/src/error.rs::AppError` — error type for file loading failures
- `common/src/lib.rs` — module registration pattern

## Acceptance Criteria
- [ ] `LicensePolicy` struct exists with allowlist, denylist, and default_compliant fields
- [ ] `load_from_file` loads and deserializes policy from a JSON file
- [ ] `is_compliant` correctly evaluates licenses against the policy rules
- [ ] Module is exported from `common/src/lib.rs`

## Test Requirements
- [ ] Unit test: `is_compliant` returns true for allowed licenses
- [ ] Unit test: `is_compliant` returns false for denied licenses
- [ ] Unit test: `is_compliant` returns `default_compliant` value for unlisted licenses
- [ ] Unit test: `load_from_file` handles missing or malformed policy files with appropriate errors

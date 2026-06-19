## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This provides the foundation for the license compliance report to flag packages with policy-violating licenses.

## Files to Create
- `common/src/license_policy.rs` -- License policy struct, deserialization, and loading logic
- `etc/license-policy.json` -- Default license policy configuration file

## Files to Modify
- `common/src/lib.rs` -- Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` -- Add serde_json dependency if not already present

## Implementation Notes
- Define a `LicensePolicy` struct with fields for `allowed_licenses: Vec<String>` and `denied_licenses: Vec<String>`. A license is compliant if it appears in the allowed list or does not appear in the denied list (depending on policy mode).
- Follow the existing module pattern in `common/src/` -- see `common/src/error.rs` for a reference on how shared types are structured.
- Use `serde::Deserialize` for JSON deserialization, consistent with the existing Cargo workspace dependencies.
- The default policy file (`etc/license-policy.json`) should include common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and common copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as denied, serving as a sensible default.
- Include a `LicensePolicy::load(path: &Path) -> Result<Self>` method for loading from a file path.
- All error handling must use `Result<T, AppError>` with `.context()` wrapping per the existing pattern in `common/src/error.rs`.

## Reuse Candidates
- `common/src/error.rs::AppError` -- Use existing error type for all error returns

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] Default `etc/license-policy.json` file exists with sensible defaults
- [ ] `LicensePolicy::load()` returns an error with context when the file is missing or malformed
- [ ] A license can be checked against the policy to determine compliance

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON string into `LicensePolicy`
- [ ] Unit test: `LicensePolicy::load()` returns an error for a nonexistent file path
- [ ] Unit test: check compliance for an allowed license returns true
- [ ] Unit test: check compliance for a denied license returns false

## Verification Commands
- `cargo test -p common` -- all tests pass including new license policy tests

## Dependencies
- None

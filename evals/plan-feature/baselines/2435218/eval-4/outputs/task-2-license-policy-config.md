# Task 2 — Add license policy configuration

## Repository
trustify-backend

## Description
Add a configurable license policy mechanism that defines which licenses are considered compliant. The policy is stored as a JSON configuration file in the repository and loaded at service initialization. This policy is used by the license report service to flag non-compliant license groups.

## Files to Create
- `common/src/license_policy.rs` — define `LicensePolicy` struct and loading logic
- `license-policy.json` — default license policy configuration file at the repository root

## Files to Modify
- `common/src/lib.rs` — add module declaration for `license_policy`
- `common/Cargo.toml` — add dependencies if needed (e.g., for file loading)

## Implementation Notes
- The `LicensePolicy` struct should contain:
  - `allowed_licenses: Vec<String>` — list of SPDX license identifiers that are considered compliant (allowlist approach)
  - Optionally `denied_licenses: Vec<String>` — explicit denylist for licenses that are never compliant, regardless of allowlist
- The policy loader should read the JSON file from a configurable path (environment variable or config parameter) with a sensible default pointing to the repo root's `license-policy.json`.
- Follow the error handling pattern used throughout the codebase: return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs` for the `AppError` enum.
- Place this in `common/` because it is a cross-cutting utility that the SBOM service will consume, following the same pattern as other shared utilities in `common/src/`.
- The default `license-policy.json` should include common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed, providing a reasonable starting point.
- A license is compliant if it appears in `allowed_licenses` and does not appear in `denied_licenses`. If `allowed_licenses` is empty, all licenses not in `denied_licenses` are considered compliant.

## Reuse Candidates
- `common/src/error.rs::AppError` — error type for wrapping policy loading failures
- `common/src/db/mod.rs` — reference for how common modules are structured and exported

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed_licenses` and `denied_licenses` fields
- [ ] Policy can be loaded from a JSON file path
- [ ] A default `license-policy.json` file exists at the repository root with common permissive licenses
- [ ] Policy loading errors are wrapped in `AppError` with descriptive context
- [ ] `LicensePolicy` exposes a method to check whether a given license identifier is compliant
- [ ] Project compiles without errors

## Test Requirements
- [ ] Unit test: loading a valid policy JSON file produces the correct `LicensePolicy` struct
- [ ] Unit test: `is_compliant("MIT")` returns `true` when MIT is in the allowed list
- [ ] Unit test: `is_compliant("GPL-3.0")` returns `false` when GPL-3.0 is not in the allowed list
- [ ] Unit test: `is_compliant` correctly handles the denied list taking precedence over the allowed list
- [ ] Unit test: loading a malformed JSON file returns an appropriate error

## Verification Commands
- `cargo check -p trustify-common` — compiles without errors
- `cargo test -p trustify-common` — all tests pass

## Documentation Updates
- `README.md` — document the license policy configuration file format, location, and customization instructions

# Task 1 — Add license policy configuration model and loader

## Repository
trustify-backend

## Description
Introduce a license policy configuration mechanism that defines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This provides the foundation for license compliance checking in the license report endpoint.

## Files to Modify
- `common/src/lib.rs` — re-export the new `license_policy` module

## Files to Create
- `common/src/license_policy/mod.rs` — LicensePolicy struct, deserialization from JSON, policy lookup methods
- `license-policy.json` — default license policy configuration file at the repository root (or a `config/` directory if one exists)

## Implementation Notes
- Define a `LicensePolicy` struct containing:
  - `allowed_licenses: Vec<String>` — SPDX identifiers of licenses that are compliant (e.g., "MIT", "Apache-2.0")
  - `denied_licenses: Vec<String>` — SPDX identifiers explicitly flagged as non-compliant
  - A method `is_compliant(&self, license: &str) -> bool` that returns `true` if the license is in the allowed list or not in the denied list
- Use `serde` and `serde_json` for deserialization, following the same patterns used in existing configuration loading in the codebase
- Follow the error handling pattern from `common/src/error.rs` — return `Result<T, AppError>` with `.context()` wrapping for file I/O errors
- The policy file path should be configurable (e.g., via environment variable or CLI argument), with a sensible default

## Reuse Candidates
- `common/src/error.rs::AppError` — reuse the existing error enum for policy loading errors

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly classifies licenses as compliant or non-compliant
- [ ] Missing or malformed policy files produce clear error messages using `AppError`
- [ ] A default `license-policy.json` file is included with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON and verify `is_compliant()` returns correct results for allowed, denied, and unlisted licenses
- [ ] Unit test: loading a malformed JSON file returns an appropriate error
- [ ] Unit test: loading a nonexistent file returns an appropriate error

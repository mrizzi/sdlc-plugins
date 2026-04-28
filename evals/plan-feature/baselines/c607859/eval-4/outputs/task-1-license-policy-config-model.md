# Task 1 -- License Policy Configuration Model

## Repository
trustify-backend

## Description
Define a license policy configuration model that loads and validates a JSON policy file specifying which SPDX license identifiers are allowed and which are denied. This provides the foundation for evaluating license compliance in the report endpoint. The policy file is stored in the repository and loaded at startup, enabling organizations to customize their compliance rules without code changes.

## Files to Create
- `common/src/model/license_policy.rs` -- `LicensePolicy` struct with `allowed` and `denied` license identifier lists, JSON deserialization, and a `is_compliant(license: &str) -> bool` method
- `license-policy.json` -- Default policy configuration file at the repository root with a starter set of allowed licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC) and denied licenses (GPL-2.0-only, GPL-3.0-only, AGPL-3.0-only)

## Files to Modify
- `common/src/model/mod.rs` -- Add `pub mod license_policy;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` (see `paginated.rs` for the established struct + derive macro pattern)
- Use `serde::Deserialize` for JSON parsing, consistent with the rest of the codebase
- The `LicensePolicy` struct should contain:
  - `allowed: Vec<String>` -- list of allowed SPDX license identifiers
  - `denied: Vec<String>` -- list of denied SPDX license identifiers
- The `is_compliant` method should check: if a license is in the `denied` list, return `false`; if the `allowed` list is non-empty and the license is not in it, return `false`; otherwise return `true`
- Load the policy file path from an environment variable or config, with a fallback to `license-policy.json` at the project root
- Use `AppError` from `common/src/error.rs` for error handling when the policy file is missing or malformed
- Per constraints doc section 5.2: inspect existing code patterns in `common/src/model/` before implementing
- Per constraints doc section 5.4: reuse existing error types from `common/src/error.rs` rather than creating new error enums

## Reuse Candidates
- `common/src/error.rs::AppError` -- existing error enum for propagating config load failures
- `common/src/model/paginated.rs` -- reference pattern for struct definitions with serde derives

## Acceptance Criteria
- [ ] `LicensePolicy` struct deserializes correctly from a JSON file with `allowed` and `denied` fields
- [ ] `is_compliant` returns `true` for licenses in the allowed list
- [ ] `is_compliant` returns `false` for licenses in the denied list
- [ ] `is_compliant` returns `false` for licenses not in the allowed list when the allowed list is non-empty
- [ ] Loading a missing or malformed policy file returns a descriptive `AppError`
- [ ] A default `license-policy.json` file exists with a reasonable starter policy

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON and verify `allowed` and `denied` fields
- [ ] Unit test: `is_compliant` correctly evaluates licenses against allowed/denied lists
- [ ] Unit test: loading a non-existent policy file returns an appropriate error
- [ ] Unit test: loading a malformed JSON file returns a parse error

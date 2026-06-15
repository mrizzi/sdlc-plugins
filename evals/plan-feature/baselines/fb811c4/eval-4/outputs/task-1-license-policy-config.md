## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are approved, denied, or require review. The policy is loaded from a JSON config file at the repository root and parsed into a Rust struct for use by the license report service.

The policy file should support:
- A list of approved SPDX license identifiers (packages with these licenses are compliant)
- A list of denied SPDX license identifiers (packages with these licenses are non-compliant)
- A default disposition for licenses not in either list (e.g., "review" or "deny")

## Files to Create
- `license-policy.json` — Default license policy config at the repo root with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as approved and a sample denied list (GPL-3.0-only, AGPL-3.0-only)
- `common/src/license_policy.rs` — `LicensePolicy` struct with `approved: Vec<String>`, `denied: Vec<String>`, `default_disposition: Disposition` enum. Include a `load_from_file` function and an `evaluate(&self, license: &str) -> Compliance` method

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` declaration

## Implementation Notes
- Use `serde` and `serde_json` for deserialization of the policy file, consistent with existing patterns in the codebase
- The `Disposition` enum should have variants: `Approved`, `Denied`, `Review`
- The `evaluate` method checks the license string against approved list first, then denied list, then falls back to default disposition
- License matching should be case-insensitive to handle variations in SPDX identifiers
- Load the policy file path from an environment variable (e.g., `TRUSTIFY_LICENSE_POLICY_PATH`) with a fallback to `./license-policy.json`

Per CONVENTIONS.md: Error handling should use `AppError` with `.context()` wrapping for file I/O errors when loading the policy file. Applies: task creates `common/src/license_policy.rs` which uses the shared error type from `common/src/error.rs`.

## Acceptance Criteria
- A `LicensePolicy` struct can be deserialized from a JSON file
- The `evaluate` method correctly classifies licenses as approved, denied, or review-needed
- Missing or malformed policy files produce clear error messages via `AppError`
- Unit tests cover: approved license returns compliant, denied license returns non-compliant, unknown license uses default disposition

## Test Requirements
- Unit tests in `common/src/license_policy.rs` (inline `#[cfg(test)]` module)
- Test deserialization of a valid policy JSON
- Test `evaluate` with approved, denied, and unknown license identifiers
- Test case-insensitive matching (e.g., "mit" matches "MIT")
- Test error on missing file and malformed JSON

## Dependencies
- Depends on: None (first task)

[sdlc-workflow] Description digest: sha256-md:6bd849c9fb3ced10e18134ef35c043896397fc220ebfb6f0267e0f3ee190e93b

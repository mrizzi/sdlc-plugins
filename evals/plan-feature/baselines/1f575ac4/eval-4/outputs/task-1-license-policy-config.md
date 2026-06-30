# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant. The policy is stored as a JSON configuration file in the repository and loaded at service startup. This provides the foundation for the license compliance report to flag packages with non-compliant licenses.

## Files to Create
- `common/src/license_policy.rs` — License policy model (struct definitions for policy rules, deserialization from JSON, and a method to check if a given license identifier is compliant)
- `license-policy.json` — Default license policy configuration file at the repository root, containing an allowlist/denylist of SPDX license identifiers

## Files to Modify
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present (for JSON deserialization of the policy file)

## Implementation Notes
- Follow the existing module pattern in `common/src/` — see `common/src/error.rs` for the established single-file module style within the common crate.
- The policy struct should support both an allowlist model (only listed licenses are compliant) and a denylist model (all licenses are compliant except those listed), selectable via a field in the JSON config.
- Use `serde::Deserialize` for the policy struct, consistent with other model types in the codebase (e.g., `common/src/model/paginated.rs` uses serde derives).
- License identifiers should follow the SPDX license list format (e.g., "MIT", "Apache-2.0", "GPL-3.0-only").
- Include a `check_compliance(&self, license_id: &str) -> bool` method on the policy struct.
- Load the policy file path from configuration or default to `license-policy.json` at the repo root.

## Reuse Candidates
- `common/src/model/paginated.rs` — Demonstrates the serde derive pattern used for model structs in the common crate.
- `common/src/error.rs` — Shows the `AppError` enum pattern; the policy module should define a variant or use existing error types for policy loading failures.

## Acceptance Criteria
- [ ] A `LicensePolicy` struct exists in `common/src/license_policy.rs` with serde deserialization support
- [ ] The struct supports both allowlist and denylist compliance checking modes
- [ ] A `check_compliance` method returns `true` for compliant licenses and `false` for non-compliant ones
- [ ] A default `license-policy.json` file exists with a reasonable set of common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed
- [ ] Policy loading failures produce a clear error using the existing `AppError` pattern

## Test Requirements
- [ ] Unit test: `check_compliance` returns `true` for a license in the allowlist
- [ ] Unit test: `check_compliance` returns `false` for a license not in the allowlist (when using allowlist mode)
- [ ] Unit test: `check_compliance` returns `false` for a license in the denylist (when using denylist mode)
- [ ] Unit test: Policy deserialization succeeds for a valid JSON policy file
- [ ] Unit test: Policy deserialization returns an error for malformed JSON

## Dependencies
- None

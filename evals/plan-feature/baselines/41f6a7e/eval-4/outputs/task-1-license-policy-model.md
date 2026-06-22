# Task 1 — Add license policy configuration model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the license policy configuration model that defines which licenses are allowed, denied, or flagged for review. The policy is stored as a JSON configuration file in the repository and loaded at startup. This is the foundation for the compliance checking logic in subsequent tasks.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct with allowed/denied/review license lists, deserialized from JSON config
- `config/license-policy.json` — Default license policy configuration file with common permissive licenses (MIT, Apache-2.0, BSD) as allowed and example restricted licenses (GPL-3.0, AGPL-3.0) as denied

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/src/lib.rs` — Ensure model module is re-exported if not already

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` — see `paginated.rs` for struct definition conventions
- Use `serde::Deserialize` for JSON deserialization of the policy config, consistent with how the rest of the codebase uses serde
- The LicensePolicy struct should contain:
  - `allowed: Vec<String>` — licenses that are compliant
  - `denied: Vec<String>` — licenses that are non-compliant
  - `review: Vec<String>` — licenses requiring manual review
  - `default_policy: PolicyAction` enum (Allow, Deny, Review) for licenses not in any list
- Use SPDX license identifiers (e.g., "MIT", "Apache-2.0", "GPL-3.0-only") as the canonical format
- Include a `LicensePolicy::load(path: &Path) -> Result<Self, AppError>` method for loading from a file path
- Per docs/constraints.md section 5.2: inspect existing code patterns before implementing
- Per docs/constraints.md section 5.4: reuse existing error types from `common/src/error.rs` (AppError) rather than defining new error types

## Reuse Candidates
- `common/src/error.rs::AppError` — existing error enum for consistent error handling; use for policy file load errors
- `common/src/model/paginated.rs` — reference for struct definition patterns and serde derives in the common module

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON configuration file
- [ ] Default license-policy.json is valid and contains reasonable defaults for common OSS licenses
- [ ] PolicyAction enum supports Allow, Deny, and Review actions
- [ ] Loading a missing or malformed policy file returns a descriptive AppError

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON and verify all fields
- [ ] Unit test: deserialize policy with missing optional fields uses correct defaults
- [ ] Unit test: loading a non-existent policy file returns an appropriate error

## Dependencies
- None

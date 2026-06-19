## Repository
trustify-backend

## Target Branch
main

## Description
Define the license policy configuration model that determines which licenses are compliant and which are not. The policy is stored as a JSON configuration file in the repository root and loaded at application startup. This task establishes the foundational data structures that the license report service will use to evaluate compliance.

## Files to Modify
- `common/src/lib.rs` -- Add `license_policy` module declaration

## Files to Create
- `common/src/license_policy/mod.rs` -- LicensePolicy struct with `allowed`, `denied`, and `unknown_action` fields; deserialization from JSON; policy evaluation method `is_compliant(license: &str) -> ComplianceStatus`
- `license-policy.json` -- Default license policy configuration with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed, and known copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as flagged for review

## API Changes
- None (internal model only)

## Implementation Notes
- Follow the existing module pattern in `common/src/` for adding new modules
- The `LicensePolicy` struct should derive `Deserialize`, `Clone`, and `Debug`
- `ComplianceStatus` should be an enum with variants: `Compliant`, `NonCompliant(String)`, `Unknown`
- The policy JSON schema should include a `version` field for future schema evolution
- Use `serde_json` for deserialization, consistent with existing crate dependencies
- Policy should support both allowlist and denylist modes: if `allowed` is non-empty, only those licenses are compliant; if `denied` is non-empty, those licenses are non-compliant and all others are compliant
- Load the policy file path from environment variable `TRUST_LICENSE_POLICY_PATH` with a default fallback to `license-policy.json`

## Acceptance Criteria
- [ ] `LicensePolicy` struct can be deserialized from a JSON file
- [ ] `is_compliant()` correctly evaluates licenses against the policy
- [ ] Default `license-policy.json` file is valid and parseable
- [ ] Policy handles case-insensitive license matching (e.g., "MIT" and "mit" are equivalent)
- [ ] Unknown licenses (not in allowed or denied lists) return `ComplianceStatus::Unknown`

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON
- [ ] Unit test: `is_compliant` returns `Compliant` for an allowed license
- [ ] Unit test: `is_compliant` returns `NonCompliant` for a denied license
- [ ] Unit test: `is_compliant` returns `Unknown` for an unrecognized license
- [ ] Unit test: case-insensitive matching works correctly
- [ ] Unit test: malformed JSON returns a meaningful error

## Dependencies
- None

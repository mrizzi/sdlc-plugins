## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant for the organization. The policy is loaded from a JSON configuration file in the repository and provides the evaluation logic used by the license report service to flag policy violations.

## Files to Create
- `common/src/model/license_policy.rs` — LicensePolicy struct and deserialization logic for the JSON policy config
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `common/src/model/mod.rs` — Add `pub mod license_policy;` to expose the new module
- `common/Cargo.toml` — Add serde_json dependency if not already present

## Implementation Notes
- Follow the existing model pattern in `common/src/model/` (see `paginated.rs` for struct + derive conventions)
- The LicensePolicy struct should contain:
  - `allowed_licenses: Vec<String>` — SPDX identifiers of licenses considered compliant (e.g., "MIT", "Apache-2.0")
  - `denied_licenses: Vec<String>` — SPDX identifiers explicitly denied
  - Evaluation logic: a license is compliant if it appears in `allowed_licenses` OR does not appear in `denied_licenses` (allow-list takes precedence; if both lists are empty, all licenses are compliant by default)
- Use `serde::Deserialize` for JSON deserialization, consistent with existing patterns
- The policy file path should be configurable but default to `license-policy.json` at the repo root
- Per docs/constraints.md §5.4: reuse existing serde patterns from `common/` rather than introducing new serialization approaches

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — demonstrates the struct + Serialize/Deserialize derive pattern used in this crate
- `common/src/error.rs::AppError` — error handling pattern for policy file loading failures

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON file
- [ ] A default `license-policy.json` file exists with a reasonable set of common OSS-compliant licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and a denied list (GPL-3.0, AGPL-3.0)
- [ ] Policy evaluation correctly identifies compliant and non-compliant licenses

## Test Requirements
- [ ] Unit test: deserialize a valid policy JSON and verify fields
- [ ] Unit test: evaluate a license against the policy — compliant case
- [ ] Unit test: evaluate a license against the policy — non-compliant case
- [ ] Unit test: evaluate a license not in either list — defaults to compliant
- [ ] Unit test: handle malformed policy JSON with a descriptive error

[sdlc-workflow] Description digest: sha256:66398bde4de8c7c68205530eabfc5368be0be93de2801ced9e84edda2a3bb68c

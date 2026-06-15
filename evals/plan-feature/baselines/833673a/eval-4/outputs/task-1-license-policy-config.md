## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model and loader that reads a JSON policy file defining which licenses are compliant and which are not. The policy file specifies allowed and denied license identifiers (SPDX format). This configuration is consumed by the license report service to determine compliance status for each package license.

## Files to Create
- `modules/fundamental/src/license/mod.rs` — License module root, re-exports policy types
- `modules/fundamental/src/license/model/mod.rs` — Model module root
- `modules/fundamental/src/license/model/policy.rs` — LicensePolicy struct and LicensePolicyGroup with serialization/deserialization
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `modules/fundamental/src/lib.rs` — Register the new license module

## Implementation Notes
Follow the existing module pattern used by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/` — each domain module has `model/`, `service/`, and `endpoints/` subdirectories. This task creates only the `model/` layer for the license policy.

The `LicensePolicy` struct should include:
- `allowed_licenses: Vec<String>` — SPDX identifiers considered compliant (e.g., "MIT", "Apache-2.0")
- `denied_licenses: Vec<String>` — SPDX identifiers considered non-compliant (e.g., "GPL-3.0-only")
- `default_compliance: bool` — whether unlisted licenses are considered compliant or not

Use `serde` for JSON deserialization, consistent with existing SeaORM entity patterns in `entity/src/`. The policy loader should read from a configurable file path, defaulting to `license-policy.json` at the repository root.

Error handling must follow the project convention: return `Result<T, AppError>` with `.context()` wrapping, as established in `common/src/error.rs`.

## Reuse Candidates
- `common/src/error.rs::AppError` — reuse the shared error type for policy loading failures

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed_licenses`, `denied_licenses`, and `default_compliance` fields
- [ ] Policy can be deserialized from a JSON file using serde
- [ ] A default `license-policy.json` file exists at the repository root with a reasonable default policy
- [ ] Policy loader returns `AppError` on missing or malformed config files
- [ ] License module is registered in `modules/fundamental/src/lib.rs`

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON into `LicensePolicy` struct
- [ ] Unit test: deserialize policy with empty allowed/denied lists
- [ ] Unit test: policy loader returns error for missing file
- [ ] Unit test: policy loader returns error for malformed JSON

[sdlc-workflow] Description digest: sha256-md:6054affabf6ebd59ca7cd48ce1ba34d72f3b3540ce6033da6e199274da16648c

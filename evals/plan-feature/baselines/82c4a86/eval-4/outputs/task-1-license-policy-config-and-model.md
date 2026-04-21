# Task 1 — Add license policy configuration and model types

## Repository
trustify-backend

## Description
Define the license compliance data model types (LicenseGroup, LicenseComplianceReport, LicensePolicy) and add support for loading a configurable license policy from a JSON file. The policy file specifies which licenses are allowed, denied, or flagged for review. This task provides the foundation data structures that the report service (Task 2) and endpoint (Task 3) build upon.

## Files to Create
- `modules/fundamental/src/license/mod.rs` — License module root, re-exports model, service, and endpoints submodules
- `modules/fundamental/src/license/model/mod.rs` — Model submodule root, re-exports types
- `modules/fundamental/src/license/model/report.rs` — LicenseGroup and LicenseComplianceReport structs with Serialize derives
- `modules/fundamental/src/license/model/policy.rs` — LicensePolicy struct with Deserialize, a `load_from_file` function, and a `is_compliant(license: &str) -> bool` method
- `license-policy.json` — Default license policy configuration file at repository root

## Files to Modify
- `modules/fundamental/src/lib.rs` — Register the new `license` module

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/` for the canonical example.
- The `LicenseComplianceReport` struct should contain `groups: Vec<LicenseGroup>`. Each `LicenseGroup` has fields: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`.
- The `LicensePolicy` struct should deserialize from JSON with fields `allowed_licenses: Vec<String>` and `denied_licenses: Vec<String>`. Compliance logic: a license is non-compliant if it appears in `denied_licenses`, or (when `allowed_licenses` is non-empty) does not appear in `allowed_licenses`.
- Reuse the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` -- it already includes a `license` field, so no new package type is needed.
- Per CONVENTIONS.md Key Conventions: follow the `model/ + service/ + endpoints/` directory structure. See `modules/fundamental/src/sbom/model/summary.rs` for the established struct definition pattern.
- Per constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits, reference TC-9004 in the footer, and include the `Assisted-by: Claude Code` trailer.
- Per constraints.md section 5 (Code Change Rules): do not modify files outside the scope of this task; inspect existing code before modifying.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already contains a `license` field; reuse as the package representation within license groups rather than creating a new struct
- `common/src/error.rs::AppError` — reuse for error handling in policy loading (file not found, invalid JSON)

## Acceptance Criteria
- [ ] LicenseGroup struct defined with fields: license (String), packages (Vec<PackageSummary>), compliant (bool)
- [ ] LicenseComplianceReport struct defined with field: groups (Vec<LicenseGroup>)
- [ ] LicensePolicy struct defined with allowed_licenses and denied_licenses fields
- [ ] LicensePolicy can be deserialized from a JSON file
- [ ] Default license-policy.json file exists at repository root with a reasonable default policy (e.g., common permissive licenses allowed, known copyleft licenses flagged)
- [ ] A policy evaluation method correctly determines compliance for a given license string

## Test Requirements
- [ ] Unit test: LicensePolicy correctly identifies a denied license as non-compliant
- [ ] Unit test: LicensePolicy correctly identifies an allowed license as compliant
- [ ] Unit test: LicensePolicy with empty allowed_licenses list treats all non-denied licenses as compliant
- [ ] Unit test: LicensePolicy deserialization from valid JSON succeeds
- [ ] Unit test: LicensePolicy deserialization from invalid JSON returns an appropriate error

## Verification Commands
- `cargo test --package fundamental -- license::model` — all model and policy unit tests pass

## Documentation Updates
- `README.md` — Add section describing the license policy configuration format (JSON schema) and file location

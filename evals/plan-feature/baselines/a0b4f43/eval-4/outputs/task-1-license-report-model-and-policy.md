## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report model types and configurable license policy infrastructure. This task creates the data structures for the license compliance report (LicenseGroup, LicenseReport) and the license policy configuration that defines which licenses are allowed, denied, or flagged for review. The policy is loaded from a JSON config file in the repository, enabling organizations to customize their compliance rules.

## Files to Create
- `modules/fundamental/src/license_report/mod.rs` — Module root for the license report feature, re-exports model, service, and endpoints sub-modules
- `modules/fundamental/src/license_report/model/mod.rs` — Model module root with re-exports
- `modules/fundamental/src/license_report/model/report.rs` — LicenseReport and LicenseGroup structs with serde Serialize/Deserialize derives
- `modules/fundamental/src/license_report/model/policy.rs` — LicensePolicy struct and policy loading logic from JSON config
- `license-policy.json` — Default license policy configuration file (allowed licenses, denied licenses, review-required licenses)

## Files to Modify
- `modules/fundamental/src/lib.rs` — Add `pub mod license_report;` to register the new module
- `modules/fundamental/Cargo.toml` — Add any new dependencies if needed (likely none beyond existing serde)

## Implementation Notes
- Follow the existing module pattern used by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/` — each domain has `model/`, `service/`, and `endpoints/` sub-directories.
- The `LicenseReport` struct should contain: `sbom_id`, `generated_at` timestamp, `groups: Vec<LicenseGroup>`, `policy_violations: usize` (count of non-compliant groups).
- The `LicenseGroup` struct should contain: `license: String` (SPDX identifier), `packages: Vec<PackageSummary>`, `compliant: bool` (determined by policy).
- Reuse the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` which already includes a `license` field.
- The `LicensePolicy` struct should define: `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`, `default_policy: PolicyAction` (allow/deny/review). When a license appears in `denied_licenses`, the group is marked `compliant: false`. When a license appears in `allowed_licenses`, it is `compliant: true`. Otherwise, `default_policy` applies.
- Load the policy from a JSON config file path configurable via environment variable or constructor parameter.
- Per `docs/constraints.md` §5 (Code Change Rules): Changes must be scoped to the files listed. Implementation must follow the patterns referenced in these notes.
- Per `docs/constraints.md` §2 (Commit Rules): Every commit must reference TC-9004 in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per `docs/constraints.md` §3 (PR Rules): The branch must be named after the Jira issue ID, and PR link must be posted to Jira after opening.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Existing package summary struct that includes the `license` field; reuse directly in LicenseGroup.packages rather than creating a new type
- `common/src/error.rs::AppError` — Existing error enum for error handling; use for policy loading failures

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with serde derives and appropriate field types
- [ ] `LicensePolicy` struct is defined with allowed/denied license lists and default policy action
- [ ] Policy can be loaded from a JSON config file at a configurable path
- [ ] A default `license-policy.json` file exists in the repository root with a reasonable default policy
- [ ] The `license_report` module is registered in `modules/fundamental/src/lib.rs`
- [ ] All new types compile without errors

## Test Requirements
- [ ] Unit test: `LicensePolicy` correctly loads from a valid JSON file
- [ ] Unit test: `LicensePolicy` returns an error for malformed JSON
- [ ] Unit test: `LicensePolicy::is_compliant("MIT")` returns the correct result based on allowed/denied lists
- [ ] Unit test: Default policy action is applied when a license is not in allowed or denied lists

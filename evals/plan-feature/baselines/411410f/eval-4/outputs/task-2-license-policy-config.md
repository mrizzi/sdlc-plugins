# Task 2: Implement license compliance policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance policy configuration system. The policy defines which licenses are considered compliant and which are denied. It is stored as a JSON configuration file in the repository root and loaded at service startup. This allows organizations to customize their compliance rules.

## Files to Create
- `license-policy.json` — Default license compliance policy file with allowed and denied license lists
- `modules/fundamental/src/sbom/service/license_policy.rs` — Policy loading and evaluation logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_policy;` declaration

## Implementation Notes
- The `license-policy.json` file should follow this structure:
  ```json
  {
    "defaultPolicy": "allow",
    "denied": ["GPL-3.0-only", "AGPL-3.0-only", "SSPL-1.0"],
    "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0"]
  }
  ```
- `defaultPolicy` can be `"allow"` (permit unless denied) or `"deny"` (deny unless explicitly allowed).
- Create a `LicensePolicy` struct in `modules/fundamental/src/sbom/service/license_policy.rs` with:
  - Fields: `default_policy: PolicyDefault`, `denied: HashSet<String>`, `allowed: HashSet<String>`
  - Method `is_compliant(&self, license: &str) -> bool` that evaluates a license identifier against the policy
  - Method `load_from_file(path: &Path) -> Result<Self, AppError>` for loading the JSON config
- Follow error handling patterns from `common/src/error.rs`, wrapping I/O errors with `.context()`.
- Reference the service module pattern from `modules/fundamental/src/sbom/service/sbom.rs` for module structure conventions.

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root with a sensible default policy
- [ ] `LicensePolicy` struct can load and parse the JSON configuration
- [ ] `is_compliant()` correctly evaluates licenses under both `allow` and `deny` default policies
- [ ] Module is publicly exported from `modules/fundamental/src/sbom/service/mod.rs`

## Test Requirements
- [ ] Unit test: license in the `denied` list returns `compliant = false` under `defaultPolicy: "allow"`
- [ ] Unit test: license in the `allowed` list returns `compliant = true` under `defaultPolicy: "deny"`
- [ ] Unit test: unknown license returns `true` under `defaultPolicy: "allow"` and `false` under `defaultPolicy: "deny"`
- [ ] Unit test: policy loads correctly from a valid JSON file
- [ ] Unit test: policy loading returns appropriate error for malformed JSON

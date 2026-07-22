# Task 1: Define license compliance report model types

- **Jira parent**: TC-9004
- **Repository**: trustify-backend
- **Target Branch**: main
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Description

Define the Rust model types for the license compliance report response. The report groups packages by license type and includes a compliance flag per group based on a configurable license policy.

The response structure for `GET /api/v2/sbom/{id}/license-report` is:

```json
{
  "groups": [
    {
      "license": "MIT",
      "packages": ["pkg-a@1.0", "pkg-b@2.3"],
      "compliant": true
    },
    {
      "license": "GPL-3.0",
      "packages": ["pkg-c@0.5"],
      "compliant": false
    }
  ]
}
```

Also define a `LicensePolicy` configuration type that represents the allow/deny rules loaded from a JSON config file.

## Files to Modify/Create

| Action | Path |
|---|---|
| Create | `modules/fundamental/src/sbom/model/license_report.rs` |
| Modify | `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` |

## Implementation Notes

- **`modules/fundamental/src/sbom/model/license_report.rs`**: Define structs `LicenseReport`, `LicenseGroup`, and `LicensePolicy`. `LicenseReport` wraps a `Vec<LicenseGroup>`. `LicenseGroup` contains `license: String`, `packages: Vec<String>`, `compliant: bool`. `LicensePolicy` contains allow/deny license identifier lists. All structs derive `Serialize`, `Deserialize`, and `Clone`.
- Follow the existing model pattern from `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`.
- `LicenseReport` will be used as the Axum JSON response body, so it must implement `Serialize`.
- `LicensePolicy` must implement `Deserialize` to support loading from a JSON config file.

## Acceptance Criteria

- `LicenseReport` and `LicenseGroup` structs are defined with `Serialize` + `Deserialize`.
- `LicensePolicy` struct is defined with fields for allow-list and deny-list of SPDX license identifiers.
- Module is exported from `modules/fundamental/src/sbom/model/mod.rs`.
- All types compile without errors.

## Test Requirements

- Unit tests in `license_report.rs` verifying serialization round-trip for `LicenseReport`.
- Unit test verifying `LicensePolicy` deserialization from a JSON string.

## Conventions Applied

- **Module pattern**: Applies: task modifies `modules/fundamental/src/sbom/model/` matching the convention's model/service/endpoints module structure scope.

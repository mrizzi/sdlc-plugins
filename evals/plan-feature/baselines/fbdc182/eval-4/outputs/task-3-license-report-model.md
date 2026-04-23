## Repository
trustify-backend

## Description
Define the Rust response model structs for the license compliance report. These types are the shared data contract used by the service layer (Task 1) and serialized to JSON by the endpoint handler (Task 4). Keeping them in `modules/fundamental/src/sbom/model/` follows the established pattern used by `SbomSummary` and `SbomDetails`.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReportResponse`, `LicenseGroup`, and `PackageRef` structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report` and re-export the public types

## Implementation Notes
Required struct definitions:

```rust
// modules/fundamental/src/sbom/model/license_report.rs

use serde::{Deserialize, Serialize};

/// Top-level response for GET /api/v2/sbom/{id}/license-report
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LicenseReportResponse {
    pub sbom_id: uuid::Uuid,
    pub groups: Vec<LicenseGroup>,
}

/// Packages sharing a single SPDX license identifier
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LicenseGroup {
    /// SPDX license expression, e.g. "MIT", "Apache-2.0", or "NOASSERTION"
    pub license: String,
    pub packages: Vec<PackageRef>,
    pub compliant: bool,
}

/// Minimal package reference included in the report
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PackageRef {
    pub purl: String,
    pub name: String,
    pub version: Option<String>,
}
```

Follow the serialization conventions visible in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) — derive `Debug`, `Clone`, `Serialize`, `Deserialize`; use `uuid::Uuid` for identifiers.

Do not add any database-layer code here; this module is pure data transfer types.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — pattern for derive macros and field naming conventions
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package struct that includes the `license` field; align field naming with this type

## Acceptance Criteria
- [ ] `LicenseReportResponse`, `LicenseGroup`, and `PackageRef` are defined and publicly exported
- [ ] All three structs derive `Serialize` and `Deserialize` so they round-trip through `serde_json`
- [ ] `LicenseGroup.compliant` is a `bool` (not an `Option`)
- [ ] `LicenseGroup.license` uses the sentinel string `"NOASSERTION"` for packages without license data (documented via a code comment)
- [ ] `cargo build` succeeds with no new warnings

## Test Requirements
- [ ] Unit test: `serde_json::to_string` on a fully populated `LicenseReportResponse` produces valid JSON matching the documented response shape `{ "sbom_id": "...", "groups": [...] }`
- [ ] Unit test: `serde_json::from_str` on that JSON round-trips back to an equal struct

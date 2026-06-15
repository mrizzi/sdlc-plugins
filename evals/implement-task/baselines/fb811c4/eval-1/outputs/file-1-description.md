# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct that holds severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides a breakdown of vulnerability advisory counts by severity level,
/// enabling dashboard widgets to render severity distributions without
/// client-side counting.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Conventions Applied
- **Naming**: struct named after the domain concept (`SeveritySummary`), matching sibling pattern (`AdvisorySummary`, `SbomSummary`)
- **Derives**: `Serialize` for JSON response, `ToSchema` for OpenAPI, `Default` for zero-initialization (all severity levels default to 0), `Clone`, `Debug` for standard Rust practices
- **Documentation**: every field has a doc comment per the skill's code quality requirements
- **File location**: placed in `model/` directory following the module pattern
- **Default values**: using `#[derive(Default)]` ensures all counts start at 0 when no advisories exist at a given level (Acceptance Criterion 4)

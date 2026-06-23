# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action:** CREATE

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM. This is the JSON response body for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Conventions Applied

- **Struct naming:** Follows `<Purpose>Summary` convention seen in `AdvisorySummary`, `SbomSummary`
- **Derives:** Includes `Serialize`, `Deserialize` (for JSON), `ToSchema` (for OpenAPI), `Clone`, `Debug`, `Default` -- matching sibling model structs
- **Default derive:** Ensures all fields default to 0, satisfying acceptance criterion 4
- **Documentation:** Every field has a doc comment per the skill's code quality practices requirement
- **File naming:** Lowercase descriptive name matching sibling pattern (`summary.rs`, `details.rs`)

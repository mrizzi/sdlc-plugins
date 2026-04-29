# File 4: `modules/fundamental/src/advisory/model/severity_summary.rs`

**Action**: Create

## What Changes

Create a new response struct `SeveritySummary` that represents the aggregated advisory severity counts for a given SBOM.

## Full File Content

```rust
//! Advisory severity summary model.
//!
//! Provides the response structure for the advisory severity aggregation
//! endpoint, containing counts per severity level and a total.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for a given SBOM.
///
/// Each field represents the number of unique advisories at that severity level
/// linked to the SBOM. The `total` field is the sum of all severity counts.
/// Severity levels with no matching advisories default to 0.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with critical severity.
    pub critical: u64,
    /// Number of advisories with high severity.
    pub high: u64,
    /// Number of advisories with medium severity.
    pub medium: u64,
    /// Number of advisories with low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

## Patterns Followed

- Follows the same struct style as `SbomSummary` in `sbom/model/summary.rs` and `AdvisorySummary` in `advisory/model/summary.rs`
- Derives `Debug`, `Clone`, `Serialize`, `Deserialize` consistent with other model structs
- Derives `ToSchema` for OpenAPI spec generation (if utoipa is used in the project)
- Module-level doc comment (`//!`) describing the module purpose
- Doc comments on the struct and every public field
- `Default` implementation ensures all counts start at 0

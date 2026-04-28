# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct returned by the new severity aggregation endpoint.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Conventions Applied

- Derives match sibling model structs in `summary.rs` and `details.rs`: `Clone`, `Debug`, `Serialize`, `Deserialize`, `ToSchema`.
- Added `Default` derive so all counts initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- Doc comments follow the same style as `AdvisorySummary` and `AdvisoryDetails`.
- File is a standalone module file, consistent with `summary.rs` and `details.rs` siblings in the same `model/` directory.

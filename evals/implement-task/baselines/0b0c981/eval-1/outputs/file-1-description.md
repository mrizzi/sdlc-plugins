# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose
Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

## Rationale
- Derives match sibling model structs (`Serialize`, `Deserialize`, `Debug`, `Clone`).
- `Default` derive ensures all fields initialize to 0, satisfying the acceptance criterion that missing severity levels default to 0.
- `ToSchema` (utoipa) is included if the project uses OpenAPI generation, consistent with other model structs.
- Fields use `u32` since counts are non-negative integers; this matches typical Rust conventions for counters.
- The struct is kept flat (no nesting) to match the specified API response shape `{ critical: N, high: N, medium: N, low: N, total: N }`.

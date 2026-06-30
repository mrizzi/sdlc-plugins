# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

### Struct definition

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity
    pub critical: u64,
    /// Number of advisories with High severity
    pub high: u64,
    /// Number of advisories with Medium severity
    pub medium: u64,
    /// Number of advisories with Low severity
    pub low: u64,
    /// Total number of unique advisories
    pub total: u64,
}
```

### Design decisions

- **Derives follow sibling convention**: The derive list matches what is seen in `summary.rs` and `details.rs` model files (Serialize, Deserialize, Debug, Clone, plus utoipa::ToSchema for OpenAPI schema generation).
- **`Default` derive**: Ensures all fields default to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **`u64` field type**: Matches the count semantics; counts are always non-negative integers.
- **No constructor needed**: The struct can be built directly with struct literal syntax in the service method since all fields are public, matching the pattern in sibling model files.

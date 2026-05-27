# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

### Imports

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
```

Following the pattern from `advisory/model/summary.rs` and `advisory/model/details.rs`.

### SeveritySummary Struct

```rust
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity
    pub critical: u32,
    /// Count of advisories with High severity
    pub high: u32,
    /// Count of advisories with Medium severity
    pub medium: u32,
    /// Count of advisories with Low severity
    pub low: u32,
    /// Total count of unique advisories
    pub total: u32,
}
```

Key design decisions:
- **`Default` derive**: Ensures all counts initialize to 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.
- **`u32` type**: Unsigned integer since counts cannot be negative. `u32` is sufficient for advisory counts (max ~4 billion).
- **`ToSchema` derive**: Enables automatic OpenAPI schema generation, consistent with all other model structs in the codebase.
- **`Serialize`/`Deserialize`**: Required for JSON serialization in Axum responses and deserialization in tests.
- **Doc comments**: On each field for OpenAPI documentation.

### Constructor (optional convenience)

```rust
impl SeveritySummary {
    pub fn new(critical: u32, high: u32, medium: u32, low: u32) -> Self {
        Self {
            critical,
            high,
            medium,
            low,
            total: critical + high + medium + low,
        }
    }
}
```

This constructor auto-computes `total` from the individual counts, preventing inconsistency.

## Conventions Applied

- Derives match sibling structs (`Clone`, `Debug`, `Serialize`, `Deserialize`, `ToSchema`)
- Fields are `pub`, matching `AdvisorySummary` and `AdvisoryDetails` patterns
- File name matches the struct name in snake_case
- Module will be registered in `model/mod.rs` (see file-4-description.md)

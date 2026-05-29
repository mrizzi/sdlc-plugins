# File 4: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

Define the `SeveritySummary` response struct for the severity aggregation endpoint.

## Pre-Change Analysis

Before creating, read the sibling model file `modules/fundamental/src/advisory/model/summary.rs` to understand:
- Which derive macros are used on model structs
- The field naming and type conventions
- Any shared traits or imports

## Full File Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a given SBOM.
#[derive(Debug, Clone, Default, Serialize, Deserialize, ToSchema)]
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

## Design Notes

- `Default` derive ensures all fields initialize to 0, satisfying the acceptance criterion that missing severity levels default to 0
- `ToSchema` derive (from utoipa) enables OpenAPI schema generation, consistent with other model structs in the codebase
- Field types use `u32` since counts are non-negative integers
- The struct is intentionally flat (no nesting) to match the API contract: `{ critical: N, high: N, medium: N, low: N, total: N }`

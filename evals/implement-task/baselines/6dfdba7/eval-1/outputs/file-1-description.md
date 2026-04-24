# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Conventions Applied

- Follows the struct pattern from sibling `summary.rs` and `details.rs` in the same `model/` directory.
- Derives `serde::Serialize` and `serde::Deserialize` for automatic JSON serialization by Axum.
- Derives `Clone`, `Debug`, `Default` for standard Rust ergonomics.
- Uses `utoipa::ToSchema` if the project uses utoipa for OpenAPI spec generation (consistent with other model structs).

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for a given SBOM.
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

## Notes

- `Default` derive ensures all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist at that level.
- `u32` is sufficient for counts; no SBOM would realistically have more than ~4 billion advisories.
- The struct is intentionally flat (not nested) to match the API contract: `{ critical: N, high: N, medium: N, low: N, total: N }`.

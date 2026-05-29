# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

This is a new file. The complete contents would be:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
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

## Conventions Applied

- **Derive macros**: `Clone, Debug, Serialize, Deserialize, utoipa::ToSchema` -- matches the pattern from `advisory/model/summary.rs` and `sbom/model/summary.rs`
- **`Default` derive**: Added so all counts initialize to 0, satisfying the acceptance criterion "all severity levels default to 0 when no advisories exist"
- **`pub` field visibility**: All fields are public, matching sibling model structs
- **Doc comments**: Added `///` doc comments on the struct and fields, consistent with existing model documentation style
- **Field types**: `u32` is appropriate for non-negative counts

## Dependencies

- `serde` (already in `Cargo.toml`)
- `utoipa` (already in `Cargo.toml`)

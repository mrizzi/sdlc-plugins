# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct returned by the new advisory severity
aggregation endpoint. This struct provides severity counts per level and a total,
enabling dashboard widgets to render severity breakdowns.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a specific SBOM.
///
/// Provides per-severity-level counts (critical, high, medium, low) and a total count
/// of unique advisories linked to the SBOM. Used by dashboard widgets to render
/// severity breakdowns without client-side counting.
#[derive(Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq)]
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

## Conventions followed

- Single struct per model file (matches `summary.rs`, `details.rs` siblings)
- Derives `Serialize`, `Deserialize`, `Debug`, `Clone` (matches sibling model structs)
- Added `Default` for convenient zero-initialization in tests and service
- Added `PartialEq`, `Eq` for test assertions with `assert_eq!`
- Doc comments on struct and every field (per skill requirement for new symbols)
- File named `severity_summary.rs` matching the struct concept in snake_case

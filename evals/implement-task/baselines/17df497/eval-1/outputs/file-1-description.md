# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action:** CREATE

## Purpose

Define the `SeveritySummary` response struct representing the aggregated severity counts for advisories linked to an SBOM. This struct is the response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Struct Definition

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
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

### Design Decisions

- **Derives `Default`**: ensures all counts start at 0, satisfying the acceptance criterion that "all severity levels default to 0 when no advisories exist at that level."
- **Derives `Serialize`, `Deserialize`**: required for Axum's `Json` extractor to serialize responses and for test deserialization.
- **Derives `PartialEq`, `Eq`**: enables `assert_eq!` comparisons in tests.
- **Uses `u64` for counts**: consistent with count types in Rust and avoids negative values.
- **Documentation comments on struct and each field**: follows the code quality practice that every new struct must have documentation.

### Conventions Applied

- **File naming**: snake_case (`severity_summary.rs`) matching sibling `summary.rs`, `details.rs`
- **Struct naming**: PascalCase (`SeveritySummary`) matching `AdvisorySummary`, `SbomSummary`
- **Single struct per file**: matching the pattern in sibling model files
- **Derive order**: follows alphabetical convention observed in sibling structs

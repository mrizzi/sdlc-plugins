# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that holds per-severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
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

## Convention Conformance

- Single struct per file, matching `summary.rs` and `details.rs` siblings.
- Derives `Clone`, `Debug`, `Serialize`, `Deserialize` consistent with `AdvisorySummary` and `SbomSummary`.
- Derives `Default` so all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- Uses `u32` for counts (non-negative integers).
- File name `severity_summary.rs` follows snake_case convention.

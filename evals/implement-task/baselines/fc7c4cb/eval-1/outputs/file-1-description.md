# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

New model file defining the `SeveritySummary` response struct for the severity aggregation endpoint.

## Detailed Changes

Create a new file with the following contents:

### Struct: `SeveritySummary`

```rust
use serde::{Deserialize, Serialize};

/// Response model for the advisory severity aggregation endpoint.
///
/// Contains counts of advisories at each severity level for a given SBOM,
/// enabling dashboard widgets to render severity breakdowns without
/// client-side counting.
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u64,
    /// Number of high-severity advisories.
    pub high: u64,
    /// Number of medium-severity advisories.
    pub medium: u64,
    /// Number of low-severity advisories.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

### Design Decisions

- **Derives** `Serialize, Deserialize, Debug, Clone` following the same pattern as `AdvisorySummary` and `SbomSummary` in sibling model files.
- Uses `#[serde(rename_all = "camelCase")]` to match the JSON field naming convention used by other response models.
- Uses `u64` for counts to match Rust conventions for non-negative integer quantities.
- All fields default to 0 when constructed, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist at that level.
- Each field and the struct itself has a `///` doc comment per the skill's documentation requirements.

### Convention Conformance

- Matches the pattern in `advisory/model/summary.rs` and `sbom/model/summary.rs` for struct definition style.
- File is placed under `model/` with its own file, following the one-struct-per-file pattern seen in `summary.rs` and `details.rs`.

# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose
Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u32,
    /// Number of advisories with High severity.
    pub high: u32,
    /// Number of advisories with Medium severity.
    pub medium: u32,
    /// Number of advisories with Low severity.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Conventions Applied
- **Naming**: PascalCase struct name matching the file name (`severity_summary.rs` -> `SeveritySummary`), consistent with `AdvisorySummary` in `summary.rs` and `AdvisoryDetails` in `details.rs`.
- **Derives**: `Serialize`, `Deserialize` for JSON serialization (Axum requirement); `ToSchema` for OpenAPI spec generation; `Clone`, `Debug` for debugging; `Default` so all counts start at zero.
- **Documentation**: Every field and the struct itself have `///` doc comments per the skill's documentation requirement for new symbols.
- **Module placement**: Placed in `advisory/model/` alongside sibling model files (`summary.rs`, `details.rs`).

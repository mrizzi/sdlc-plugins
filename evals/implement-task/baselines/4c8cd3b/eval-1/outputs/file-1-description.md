# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action:** CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the severity count breakdown for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following contents:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity counts.
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

- **File naming:** lowercase snake_case matching the primary struct name (`severity_summary.rs` for `SeveritySummary`), consistent with sibling files `summary.rs` and `details.rs`.
- **Struct naming:** PascalCase with domain-relevant name, consistent with `AdvisorySummary` and `AdvisoryDetails`.
- **Derive macros:** `Serialize`, `Deserialize`, `ToSchema` for API response serialization, matching the pattern used by `AdvisorySummary` and `SbomSummary`.
- **Default derive:** `Default` is derived so all fields default to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- **Documentation:** Every struct and field has a doc comment explaining its purpose.

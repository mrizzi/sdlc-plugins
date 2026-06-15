# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

New model struct representing the severity aggregation response for advisories linked to an SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: i64,
    /// Number of advisories with High severity.
    pub high: i64,
    /// Number of advisories with Medium severity.
    pub medium: i64,
    /// Number of advisories with Low severity.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
}
```

## Conventions Applied

- **Derive macros**: `Serialize`, `Deserialize`, `Debug`, `Clone` matching sibling models (`AdvisorySummary`, `SbomSummary`). Added `Default` for zero-initialization per acceptance criteria.
- **Field type**: `i64` for count fields, matching numeric field conventions in sibling models.
- **Documentation**: Doc comment on struct and each field per Step 6 code quality requirements.
- **Naming**: PascalCase struct name following sibling pattern (`AdvisorySummary`, `AdvisoryDetails`).

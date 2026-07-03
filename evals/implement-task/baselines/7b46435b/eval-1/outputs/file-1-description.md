# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity
counts for a given SBOM. This struct is returned directly by the endpoint as JSON.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated advisory severity counts for an SBOM.
///
/// Each field represents the number of unique advisories at that severity level
/// linked to a given SBOM. The `total` field is the sum of all severity counts.
#[derive(Serialize, Deserialize, Debug, Clone, Default)]
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

## Conventions Applied

- **Derives**: `Serialize, Deserialize, Debug, Clone` matching sibling model structs (`AdvisorySummary`, `SbomSummary`). Also derives `Default` so all counts initialize to 0, satisfying the acceptance criterion that missing severity levels default to 0.
- **Field types**: `u64` for non-negative counts, consistent with count/aggregate fields in the codebase.
- **File placement**: Own file in `model/` directory, matching `summary.rs` and `details.rs` siblings.
- **Documentation**: Every field and the struct itself has a `///` doc comment per SKILL.md requirements.
- **Naming**: `SeveritySummary` follows `PascalCase` struct naming and the `<Noun>Summary` pattern used by `AdvisorySummary` and `SbomSummary`.

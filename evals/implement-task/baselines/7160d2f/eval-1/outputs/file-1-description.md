# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

**Purpose**: Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following contents:

```rust
//! Severity summary model for advisory aggregation.
//!
//! Provides a response struct that summarizes advisory severity counts
//! for a given SBOM, enabling dashboard severity breakdown widgets.

use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to 0 when no advisories exist at a given level.
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

## Conventions Followed

- **Derives**: `Serialize, Deserialize, Debug, Clone` matching sibling model structs (`AdvisorySummary`, `SbomSummary`). Added `Default` for zero-initialization, `PartialEq, Eq` for test assertions.
- **Documentation**: doc comments on the struct and every public field, per SKILL.md Step 6 code quality practices.
- **Module doc comment**: `//!` at top of file describing purpose.
- **File naming**: follows sibling pattern of descriptive lowercase snake_case (`summary.rs`, `details.rs`).
- **Field types**: `u64` for counts -- unsigned integer type appropriate for non-negative counts.

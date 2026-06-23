# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

**Purpose**: Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

This is a new file. The struct follows the pattern established by sibling model files like `summary.rs` (AdvisorySummary) and `details.rs` (AdvisoryDetails).

### Contents

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to a specific SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
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

### Conventions Applied

- **Derive macros**: `Serialize`, `Deserialize` for JSON serialization (matches sibling model structs), `ToSchema` for OpenAPI (if the project uses utoipa), `Default` for zero-initialized counts, `Clone` and `Debug` per Rust convention
- **Documentation**: doc comments on the struct and every field per the skill's "Documentation on new symbols" requirement
- **Naming**: PascalCase struct name with descriptive suffix following the pattern of `AdvisorySummary`, `SbomSummary`, `PackageSummary`
- **Field types**: `u32` for counts (non-negative integers)
- **Default implementation**: derived `Default` gives all fields `0`, satisfying acceptance criterion "All severity levels default to 0"

# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM. This struct is the response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

Create a new file with the following contents:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

- **Derive macros**: Matches sibling model structs (e.g., `SbomSummary`, `AdvisorySummary`) which derive `Clone, Debug, Serialize, Deserialize`. Added `Default` because the acceptance criteria require defaulting to zero. Added `ToSchema` for OpenAPI generation if the project uses utoipa.
- **Field types**: Uses `u64` for counts, matching Rust convention for non-negative integer counts.
- **Documentation**: Every field has a doc comment (`///`) per the skill's code quality requirements.
- **File naming**: Named `severity_summary.rs` following the pattern of `summary.rs` and `details.rs` in sibling model directories.
- **Module placement**: Located in `advisory/model/` alongside `summary.rs` and `details.rs`, following the established module pattern.

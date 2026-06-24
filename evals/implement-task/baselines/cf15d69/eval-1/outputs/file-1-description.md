# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory severity counts for a given SBOM. This struct is returned as JSON by the new endpoint.

## Detailed Changes

Create a new file with the following content:

```rust
//! Advisory severity summary model.
//!
//! Provides the [`SeveritySummary`] response struct for the advisory severity
//! aggregation endpoint.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated advisory severity counts for a single SBOM.
///
/// Each field represents the number of unique advisories at that severity level
/// linked to the SBOM. The `total` field is the sum of all severity levels.
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

## Convention Conformance

- **Derives**: Follows sibling model files (`summary.rs`, `details.rs`) which use `Serialize`, `Deserialize`, `Debug`. Added `Default` per acceptance criteria (all zeros when no advisories). Added `Clone` and `ToSchema` to match sibling patterns for API response types.
- **Documentation**: Every struct and field has a `///` doc comment per the skill's code quality requirement.
- **Naming**: File named `severity_summary.rs` following the pattern of `summary.rs` and `details.rs` in the same directory.
- **Module-level docs**: `//!` doc comment at the top of the file following Rust convention.

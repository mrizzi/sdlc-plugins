# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM. This is the response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Sibling Reference

Follows the pattern established by:
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct
- `modules/fundamental/src/advisory/model/details.rs` -- `AdvisoryDetails` struct

## Detailed Changes

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
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Convention Conformance

- Derives `Serialize`, `Deserialize` matching sibling model structs
- Derives `ToSchema` for OpenAPI documentation (if utoipa is used in the project)
- Derives `Default` to ensure all severity levels start at 0 (acceptance criterion #4)
- Uses `///` doc comments on the struct and every field (per Step 7 documentation requirements)
- Placed in its own file under `model/` following the one-struct-per-file pattern from siblings
- Uses `u32` for counts (non-negative integers)

# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM. This is the response type returned by the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Sibling Reference

Modeled after `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) and `modules/fundamental/src/advisory/model/details.rs` (`AdvisoryDetails`), which follow the same pattern of a dedicated struct file with Serde derives.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq, ToSchema)]
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

## Design Notes

- Derives `Default` to ensure all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist
- Derives `Serialize` and `Deserialize` for JSON serialization via Axum's `Json` extractor
- Derives `ToSchema` for OpenAPI spec generation if the project uses utoipa (following the pattern of other model structs)
- Uses `u32` for counts since advisory counts are non-negative integers
- Every struct and field has a documentation comment per the skill's code quality requirements
- The struct is intentionally flat (not nested) to match the expected response shape `{ critical: N, high: N, medium: N, low: N, total: N }`

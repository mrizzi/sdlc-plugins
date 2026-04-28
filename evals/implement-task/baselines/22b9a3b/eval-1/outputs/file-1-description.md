# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory severity counts for a given SBOM. This struct is returned as the JSON response body from the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Sibling Reference

Modeled after `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) and `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) which both derive serde traits and represent domain-specific response types.

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a specific SBOM.
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

## Design Notes

- `Default` derive ensures all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- `ToSchema` derive (from utoipa) is included if the project uses OpenAPI documentation generation, consistent with typical Axum+utoipa projects. If the project does not use utoipa, this derive and import would be removed.
- `u32` is used for counts since advisory counts are always non-negative and unlikely to exceed `u32::MAX`.
- The struct is intentionally flat (not nested) to match the specified API response shape: `{ critical: N, high: N, medium: N, low: N, total: N }`.

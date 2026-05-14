# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to a given SBOM.

## Detailed Changes

Create a new file with the following contents:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: u32,
    /// Count of advisories with High severity.
    pub high: u32,
    /// Count of advisories with Medium severity.
    pub medium: u32,
    /// Count of advisories with Low severity.
    pub low: u32,
    /// Total count of unique advisories (sum of all severity levels).
    pub total: u32,
}
```

## Conventions Applied

- **Derives**: `Clone, Debug, Serialize, Deserialize` matching sibling model structs like `AdvisorySummary`, `SbomSummary`. Added `Default` so all fields initialize to 0 (satisfying the acceptance criterion that severity levels default to 0). Added `ToSchema` for OpenAPI documentation generation if used.
- **Field types**: `u32` for counts (non-negative integers). Snake_case field names for Rust convention; serde will serialize as `critical`, `high`, `medium`, `low`, `total` in JSON.
- **Documentation**: Doc comments on the struct and each field, following Rust documentation conventions.
- **No `id` or `sbom_id` field**: The response is contextual to the request path parameter; including the SBOM ID in the response is unnecessary and not specified in the acceptance criteria.

# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose
Define the `SeveritySummary` response struct for the advisory severity aggregation endpoint.

## Sibling Reference
Follows the pattern of `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`)
and `modules/fundamental/src/advisory/model/details.rs` (`AdvisoryDetails`).

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Summary of advisory severity counts for an SBOM.
///
/// Provides aggregated counts of advisories by severity level (critical, high,
/// medium, low) and a total count. Used by dashboard widgets to render severity
/// breakdowns without client-side counting.
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

## Notes
- Derives `Default` so all fields initialize to 0 (satisfying acceptance criterion: "All severity levels default to 0 when no advisories exist at that level").
- Derives `Serialize`/`Deserialize` for JSON serialization via Axum's `Json` extractor.
- Derives `ToSchema` for OpenAPI spec generation (if utoipa is used in the project; omit if not).
- Each field has a doc comment per the "Code quality practices" requirement in Step 6.
- The struct-level doc comment explains what the struct is and its purpose.

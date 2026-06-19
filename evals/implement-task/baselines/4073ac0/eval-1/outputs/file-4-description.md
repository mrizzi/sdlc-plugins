# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create

## Purpose

Defines the `SeveritySummary` response struct returned by the advisory severity aggregation endpoint. This struct represents the aggregated count of advisories by severity level for a given SBOM.

## Full File Content

```rust
//! Advisory severity summary model.
//!
//! Provides the response type for the SBOM advisory severity aggregation endpoint.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
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
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

## Design Decisions

- **Derives**: `Serialize`, `Deserialize` for JSON serialization (Axum's `Json` extractor). `Clone`, `Debug` match sibling model conventions (`AdvisorySummary`, `SbomSummary`). `Default` provides zero-initialized values. `ToSchema` for OpenAPI spec generation if utoipa is used.
- **Field type `u32`**: Counts are non-negative integers. `u32` is sufficient for advisory counts (max ~4 billion).
- **Documentation**: Every field and the struct itself have doc comments, following the skill's code quality requirements for new symbols.
- **Module-level doc comment**: Provides context for the file's purpose, following Rust convention.
- **No `id` or `sbom_id` field**: The response is always scoped to a specific SBOM via the URL path parameter, so including the SBOM ID in the response would be redundant.

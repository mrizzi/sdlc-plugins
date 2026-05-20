# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to a given SBOM. This struct is returned as JSON by the new endpoint.

## Conventions Applied

- Derives `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` -- matching the pattern from sibling `summary.rs` and `details.rs` model files
- All fields are `pub` -- matching sibling model structs
- Uses `i64` for counts -- consistent with database integer types in SeaORM
- Implements `Default` to ensure zero-initialization of all severity levels

## Detailed Content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
#[derive(Debug, Clone, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: i64,
    /// Number of advisories with High severity.
    pub high: i64,
    /// Number of advisories with Medium severity.
    pub medium: i64,
    /// Number of advisories with Low severity.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
}
```

## Design Decisions

1. **`i64` for counts**: SeaORM's `COUNT(*)` returns `i64` by default. Using `i64` avoids unnecessary casting at the query layer.

2. **`Default` derive**: Provides zero-initialization so that missing severity levels automatically default to 0, satisfying the acceptance criterion "all severity levels default to 0 when no advisories exist at that level."

3. **`ToSchema` derive**: Enables automatic OpenAPI documentation generation, consistent with other model types in the codebase.

4. **No `id` or `sbom_id` field**: The response is scoped by the URL path parameter. Including the SBOM ID in the response body would be redundant and is not part of the specified API contract.

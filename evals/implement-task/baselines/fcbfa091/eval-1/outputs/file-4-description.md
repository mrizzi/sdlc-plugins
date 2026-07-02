# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM. This struct is returned by the new endpoint as JSON.

## File content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Deserialize, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Count of advisories with critical severity.
    pub critical: u32,
    /// Count of advisories with high severity.
    pub high: u32,
    /// Count of advisories with medium severity.
    pub medium: u32,
    /// Count of advisories with low severity.
    pub low: u32,
    /// Total count of unique advisories across all severity levels.
    pub total: u32,
}
```

## Design decisions

- **`Default` derive**: provides all-zero initialization, satisfying the acceptance criterion that all severity levels default to 0
- **`Serialize` + `Deserialize`**: required for JSON serialization by Axum's `Json` extractor and for test deserialization
- **`ToSchema`**: follows the OpenAPI documentation pattern seen in sibling model structs (`AdvisorySummary`, `SbomSummary`)
- **`u32` type**: counts are always non-negative; `u32` is sufficient for advisory counts and avoids unnecessary signed arithmetic
- **Documentation comments**: every struct and field has a `///` doc comment as required by the skill's code quality practices

## Conventions applied

- File placed in `model/` directory following the `model/ + service/ + endpoints/` module structure
- Struct naming uses domain noun: `SeveritySummary` (matching `AdvisorySummary`, `SbomSummary`)
- Derive macros match the set used by sibling model structs
- Public fields with doc comments

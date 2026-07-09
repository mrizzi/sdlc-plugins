# File 4: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Pre-creation inspection

Before creating this file, inspect sibling model files to match conventions:
- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` in `modules/fundamental/src/advisory/model/summary.rs` to see derive macros, field types, and documentation style.
- `mcp__serena_backend__find_symbol("AdvisoryDetails", include_body=true)` in `modules/fundamental/src/advisory/model/details.rs` for a second reference.
- `mcp__serena_backend__find_symbol("SbomSummary", include_body=true)` in `modules/fundamental/src/sbom/model/summary.rs` for cross-module model convention confirmation.

## File content

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
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

## Design decisions

- **`Default` derive**: Ensures all fields initialize to 0, satisfying the acceptance criterion "All severity levels default to 0 when no advisories exist at that level."
- **`i64` for counts**: Matches the numeric type conventions observed in sibling model structs. Could alternatively be `usize`, but `i64` aligns better with database integer types used by SeaORM.
- **`Serialize, Deserialize`**: Required for Axum's `Json<T>` response serialization and for potential request deserialization in tests.
- **`Clone, Debug`**: Standard derive macros present on all sibling model structs.
- **Documentation comments**: Every struct and field has a `///` doc comment per the SKILL.md code quality requirement.
- **No `utoipa::ToSchema`**: If sibling models derive `utoipa::ToSchema` for OpenAPI generation, this struct should too. This would be confirmed during the sibling inspection step and added if needed.

## Conventions followed

- **Derive macro order**: Matches sibling models (alphabetical: Clone, Debug, Default, Deserialize, Serialize -- or matching sibling order).
- **File location**: `modules/fundamental/src/advisory/model/severity_summary.rs` follows the `model/<name>.rs` pattern used by `summary.rs` and `details.rs`.
- **Module registration**: Registered in `model/mod.rs` (see file-3-description.md).
- **Import organization**: External crate imports (`serde`) first, matching project convention.

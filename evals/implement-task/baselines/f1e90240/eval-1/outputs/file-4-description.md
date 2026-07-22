# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: Create (new file)
**Purpose**: Define the SeveritySummary response struct

## Pre-Implementation Inspection

Before creating, would use Serena to inspect sibling model files:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct, its fields (especially the `severity` field), derive macros used
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` -- understand AdvisoryDetails struct pattern
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/model/summary.rs` -- cross-domain comparison for model struct patterns
- `mcp__serena_backend__find_symbol` on `AdvisorySummary` with `include_body=true` -- understand the severity field type and possible values

## File Contents

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level (Critical, High,
/// Medium, Low) along with a total count. Used by dashboard widgets to render
/// severity breakdowns without requiring client-side counting.
#[derive(Debug, Clone, Serialize, ToSchema)]
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

impl Default for SeveritySummary {
    fn default() -> Self {
        Self {
            critical: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0,
        }
    }
}
```

## Key Patterns Followed

- **Derive macros**: `Debug`, `Clone`, `Serialize` matching sibling model structs (AdvisorySummary, SbomSummary). `ToSchema` for OpenAPI spec generation if siblings use it.
- **Documentation**: Every struct and field has a `///` doc comment per the skill's code quality requirements.
- **Field types**: `u32` for counts (non-negative integers). Would verify against sibling patterns -- if siblings use `i64` or `usize`, match that.
- **Default implementation**: All counts initialize to 0, satisfying the acceptance criterion that "all severity levels default to 0 when no advisories exist."
- **Naming**: PascalCase struct name, snake_case field names, matching Rust conventions and sibling patterns.
- **Serialization**: Fields serialize to lowercase JSON keys matching the API spec: `{ critical: N, high: N, medium: N, low: N, total: N }`.

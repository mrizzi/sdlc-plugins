# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Detailed Changes

### Inspect before writing

Before creating this file, inspect sibling model files to confirm patterns:
- Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` to see `AdvisorySummary` struct structure and derive macros
- Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` to see `AdvisoryDetails` struct pattern
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` to see the `severity` field type (needed for counting logic)

### New file content

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated advisory severity counts for an SBOM.
///
/// Contains the count of unique advisories at each severity level
/// (Critical, High, Medium, Low) plus a total count. Used by the
/// advisory-summary endpoint to provide dashboard-ready severity breakdowns.
#[derive(Debug, Clone, Serialize, ToSchema)]
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

### Notes

- Derive macros (`Serialize`, `ToSchema`) follow the pattern observed in sibling model structs like `AdvisorySummary` and `SbomSummary`
- All fields default to 0 per acceptance criteria ("All severity levels default to 0 when no advisories exist at that level")
- `u64` used for counts — adjust if siblings use a different integer type (e.g., `i64` or `usize`)
- `ToSchema` derives OpenAPI schema generation if the project uses `utoipa` — confirm by inspecting siblings. If not used, omit.
- Every field has a doc comment per the skill's code quality requirements

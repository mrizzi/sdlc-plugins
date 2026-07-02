# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct used as the JSON response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-implementation Inspection

Before creating this file, inspect sibling model files to confirm conventions:
- Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` to see the `AdvisorySummary` struct's derive macros, field types, and doc comments
- Use `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` to confirm the pattern holds across siblings
- Confirm the `severity` field type on `AdvisorySummary` to understand what severity values are available for counting

## Planned Content

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Summary of advisory severity counts for a given SBOM.
///
/// Aggregates the number of advisories at each severity level
/// (critical, high, medium, low) linked to an SBOM, along with
/// the total count of unique advisories.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories across all severity levels.
    pub total: u32,
}
```

## Design Decisions

- **`Default` derive**: Ensures all fields default to 0 when no advisories exist, satisfying acceptance criterion "All severity levels default to 0 when no advisories exist at that level"
- **`Serialize` only (no `Deserialize`)**: This is a response-only struct; the API never receives it as input
- **`ToSchema` derive**: Following the convention if the project uses `utoipa` for OpenAPI spec generation (would confirm by inspecting sibling model structs)
- **`u32` field type**: Non-negative counts; consistent with count semantics
- **Doc comments on every field**: Per SKILL.md code quality requirements, every new public symbol gets a documentation comment

## Conventions Applied

- Derive macros match sibling model structs (`Clone, Debug, Serialize`)
- File naming follows the pattern of sibling files (`summary.rs`, `details.rs`)
- Doc comment style uses `///` per Rust convention

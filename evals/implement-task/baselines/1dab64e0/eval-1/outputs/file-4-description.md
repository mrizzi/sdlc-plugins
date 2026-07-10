# File 4: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated vulnerability advisory severity counts for a given SBOM.

## Pre-change Inspection

Before creating, inspect sibling model files to understand conventions:
```
mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)
mcp__serena_backend__find_symbol("AdvisoryDetails", include_body=true)
mcp__serena_backend__find_symbol("SbomSummary", include_body=true)
```

Understand derive macros used, field naming style, and documentation patterns.

## File Contents

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels. All fields default to 0
/// when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
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

## Design Decisions

1. **Derive macros**: `Serialize` for JSON serialization (Axum response), `Clone` and `Debug` for standard Rust conventions matching sibling structs, `Default` to ensure all fields start at 0, `ToSchema` for OpenAPI spec generation (if the project uses utoipa).

2. **Field types**: `u32` for counts -- non-negative integers, sufficient range for advisory counts. Matches Rust convention for counters.

3. **Field naming**: lowercase snake_case matching Rust convention. Serde will serialize these as-is, producing the JSON response: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`.

4. **Default trait**: Deriving `Default` ensures all fields start at 0, satisfying the acceptance criterion that all severity levels default to 0 when no advisories exist.

5. **Doc comments**: Every field and the struct itself have `///` doc comments per the SKILL.md code quality requirement.

## Notes

- The exact derive macros would be confirmed by inspecting sibling model structs (`AdvisorySummary`, `AdvisoryDetails`). If siblings do not use `ToSchema`, it would be omitted.
- If the project uses a different serialization configuration (e.g., `#[serde(rename_all = "camelCase")]`), that would be applied to match sibling structs.

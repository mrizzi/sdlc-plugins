# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents aggregated severity counts
for advisories linked to an SBOM.

## Sibling Reference

- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct
- `modules/fundamental/src/advisory/model/details.rs` -- `AdvisoryDetails` struct
- `modules/fundamental/src/sbom/model/summary.rs` -- `SbomSummary` struct

These siblings show the pattern: derive `Serialize` (and `Deserialize` if needed),
use `serde` attributes, and include doc comments on the struct and its fields.

## Detailed Changes

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Debug, Clone, Default, Serialize, ToSchema)]
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

## Conventions Applied

- **Derives**: `Debug`, `Clone`, `Default`, `Serialize` -- consistent with sibling model structs.
  `ToSchema` for OpenAPI spec generation (if utoipa is used).
- **Default**: Derives `Default` so all counts start at 0, satisfying the acceptance criterion
  that severity levels default to 0 when no advisories exist.
- **Doc comments**: `///` doc comments on the struct and every field (required by SKILL.md
  code quality practices).
- **Field types**: `u32` for counts -- non-negative integers, sufficient range.
- **No Deserialize**: This struct is response-only (outbound), so `Deserialize` is not needed.
  If sibling analysis of actual code shows that response structs also derive `Deserialize`,
  add it for consistency.

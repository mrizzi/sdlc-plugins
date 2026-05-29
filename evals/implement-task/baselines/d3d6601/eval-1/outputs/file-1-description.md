# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity-level counts.
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

## Conventions Applied

- **Derive macros**: `Serialize`, `Deserialize`, `ToSchema` match sibling model structs like `AdvisorySummary` and `SbomSummary`
- **Clone, Debug, Default**: standard derives for response structs in this codebase
- **Documentation**: `///` doc comments on the struct and every public field (per SKILL.md requirement for new symbols)
- **Naming**: PascalCase struct name following sibling pattern (`AdvisorySummary`, `SbomDetails`)
- **Default derive**: ensures all counts default to 0 when no advisories exist, satisfying acceptance criterion "All severity levels default to 0"
- **u32 type**: unsigned integer for counts (cannot be negative)

## Sibling Parity

Compared with `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` and `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`:
- Same derive macro set
- Same documentation style
- Same module structure (standalone file registered in parent `mod.rs`)

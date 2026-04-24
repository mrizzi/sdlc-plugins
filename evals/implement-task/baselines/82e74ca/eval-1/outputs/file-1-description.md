# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct is the response body for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Conventions Applied

- **Module pattern**: Follows the `model/` convention established by sibling files `summary.rs` and `details.rs`
- **Derive macros**: Uses `Serialize`, `Deserialize`, `Debug`, `Clone` consistent with `AdvisorySummary` and `AdvisoryDetails`
- **Naming**: PascalCase struct name following domain convention (`AdvisorySummary` -> `SeveritySummary`)
- **Doc comments**: Every public symbol has a documentation comment per SKILL.md requirement

## Detailed Changes

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
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

## Design Decisions

1. **`u64` for counts**: Matches the unsigned nature of counts (cannot be negative) and provides ample range.
2. **`Default` implementation**: Explicitly defaults all fields to 0, supporting the acceptance criterion "all severity levels default to 0 when no advisories exist at that level".
3. **`Serialize` + `Deserialize`**: Required for Axum's `Json` response serialization and for test deserialization.
4. **Flat struct (no nesting)**: Matches the API contract `{ critical: N, high: N, medium: N, low: N, total: N }` directly.

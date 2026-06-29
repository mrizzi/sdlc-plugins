# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

New file defining the `SeveritySummary` response struct used by the severity aggregation endpoint.

## Detailed Changes

### SeveritySummary struct

Create a new struct following the sibling model pattern from `summary.rs` and `details.rs`:

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity-level counts.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Count of advisories with Critical severity.
    pub critical: i64,
    /// Count of advisories with High severity.
    pub high: i64,
    /// Count of advisories with Medium severity.
    pub medium: i64,
    /// Count of advisories with Low severity.
    pub low: i64,
    /// Total count of unique advisories across all severity levels.
    pub total: i64,
}
```

### Default implementation

Implement `Default` for the struct so that all counts initialize to 0:

```rust
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

## Convention Compliance

- **Derive macros**: Matches sibling models (Serialize, Deserialize, Debug, Clone) with additional PartialEq, Eq for test assertions
- **Documentation**: Doc comment on struct and every public field (per SKILL.md code quality requirements)
- **Naming**: Follows `<Entity>Summary` pattern from sibling `AdvisorySummary`
- **Field types**: Uses `i64` for counts, consistent with PostgreSQL integer aggregation return types

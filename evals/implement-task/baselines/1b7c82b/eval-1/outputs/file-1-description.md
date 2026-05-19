# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity counts for advisories linked to an SBOM. This struct is the data contract for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Struct Definition

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity-level counts.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total count of unique advisories across all severity levels.
    pub total: u64,
}
```

### Design Decisions

- **Derive `Default`**: All fields default to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist at that level.
- **Derive `Serialize` and `Deserialize`**: Follows the sibling model convention (e.g., `SbomSummary`, `AdvisorySummary`) for JSON serialization via Axum.
- **Derive `PartialEq, Eq`**: Enables assertion comparisons in tests.
- **`u64` type for counts**: Matches Rust conventions for non-negative counts. Large enough for any realistic advisory count.
- **Doc comments on every field**: Follows the implement-task requirement to document every new public symbol.

### Conventions Applied

- File placement in `model/` directory follows the module pattern from siblings (`summary.rs`, `details.rs`)
- Derive macro set matches sibling model structs
- Documentation comments use `///` Rust doc comment convention

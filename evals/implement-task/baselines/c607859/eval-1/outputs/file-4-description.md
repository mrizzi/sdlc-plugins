# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Context

New model file defining the `SeveritySummary` response struct. This struct represents the
aggregated severity counts returned by the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Sibling Pattern Reference

Looking at sibling model files:
- `advisory/model/summary.rs` defines `AdvisorySummary` with `#[derive(Serialize, Deserialize, Debug, Clone)]`
- `advisory/model/details.rs` defines `AdvisoryDetails` similarly
- `sbom/model/summary.rs` defines `SbomSummary` with the same derive pattern
- All model structs use `serde` for serialization/deserialization
- All model structs have doc comments explaining what they represent

## File Contents

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts for vulnerability advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level (critical, high,
/// medium, low) and a total count. All counts default to zero when no advisories
/// exist at a given severity level.
#[derive(Serialize, Deserialize, Debug, Clone, Default, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Number of advisories with critical severity.
    pub critical: u64,

    /// Number of advisories with high severity.
    pub high: u64,

    /// Number of advisories with medium severity.
    pub medium: u64,

    /// Number of advisories with low severity.
    pub low: u64,

    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Design Decisions

- **`u64` for counts**: matches Rust conventions for non-negative counts; large enough for any realistic advisory count.
- **`Default` derive**: ensures all fields initialize to 0, satisfying the acceptance criterion that all severity levels default to 0.
- **`PartialEq, Eq` derives**: enables `assert_eq!` in tests, consistent with the test assertion pattern.
- **`Serialize, Deserialize`**: required for Axum's `Json` extractor to serialize the response body.
- **Flat struct (no nesting)**: the API contract specifies `{ critical: N, high: N, medium: N, low: N, total: N }` -- a flat JSON object, so the struct is flat.
- **Documentation comments**: every public struct and field has a doc comment, following the SKILL.md's code quality practice that "every new struct must have a documentation comment."

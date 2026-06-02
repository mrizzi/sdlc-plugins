# File 2: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct that represents aggregated severity counts for advisories linked to an SBOM.

## Contents

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a given SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// The `total` field is the sum of all severity level counts.
#[derive(Clone, Debug, Default, Deserialize, Serialize)]
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

## Design Decisions
- Derives `Default` so all counts initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
- Derives `Serialize` for JSON response serialization via Axum's `Json` extractor (consistent with `AdvisorySummary`, `SbomSummary` siblings).
- Derives `Deserialize` for use in test deserialization of response bodies.
- Uses `u32` for counts -- sufficient for advisory counts, and unsigned since counts cannot be negative.
- Fields use snake_case, matching the expected JSON response shape `{ critical: N, high: N, medium: N, low: N, total: N }`.
- Every public symbol has a `///` doc comment per the code quality practice requirement.

## Conventions Applied
- Model struct naming: PascalCase noun (`SeveritySummary`), matching `AdvisorySummary`, `SbomSummary`.
- Derive order: alphabetical (`Clone, Debug, Default, Deserialize, Serialize`), matching sibling structs.
- File naming: snake_case matching the struct name, consistent with `summary.rs`, `details.rs`.
- Documentation: `///` doc comments on struct and all public fields.

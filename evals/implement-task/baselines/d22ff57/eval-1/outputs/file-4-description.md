# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

## Action: CREATE

## Summary

Define the `SeveritySummary` response struct that represents the severity count breakdown
for advisories linked to an SBOM.

## Full File Content

```rust
use serde::{Deserialize, Serialize};

/// Summary of advisory severity counts for a given SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// All fields default to 0 when no advisories exist at the given level.
#[derive(Debug, Clone, Default, Serialize, Deserialize, PartialEq, Eq)]
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

- **`Default` derive:** Ensures all fields initialize to 0, satisfying the acceptance criterion that missing severity levels default to zero.
- **`Serialize` / `Deserialize`:** Required for Axum's `Json` extractor to serialize the response and for test deserialization.
- **`PartialEq` / `Eq`:** Enables `assert_eq!` comparisons in integration tests.
- **`u32` type:** Advisory counts are non-negative integers; `u32` provides sufficient range and matches semantic intent.
- **Documentation:** Every field has a doc comment explaining its meaning, following the code quality practice from the skill spec.

## Conventions Applied

- **Struct naming:** Uses PascalCase with descriptive suffix (`SeveritySummary`), consistent with `AdvisorySummary` and `SbomSummary`.
- **Derive macros:** Matches the derive pattern seen in sibling model structs (`Serialize`, `Deserialize`, `Debug`, `Clone`).
- **File placement:** Lives in `model/` directory alongside `summary.rs` and `details.rs`.
- **Module registration:** Will be registered via `pub mod severity_summary;` in `model/mod.rs` (File 3).

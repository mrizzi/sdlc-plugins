# File 4 -- Create: `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory
severity counts for an SBOM. This is the response body for the
`GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Pre-Implementation Inspection

Before creating, inspect sibling model files to match conventions:
- `modules/fundamental/src/advisory/model/summary.rs` -- for derive macros, doc comments,
  and field type patterns.
- `modules/fundamental/src/advisory/model/details.rs` -- for additional patterns.
- `modules/fundamental/src/sbom/model/summary.rs` -- for cross-module consistency.

## Full File Content

```rust
//! Advisory severity summary model.

use serde::{Deserialize, Serialize};

/// Aggregated advisory severity counts for an SBOM.
///
/// Contains counts of unique advisories at each severity level
/// (Critical, High, Medium, Low) plus a total count across all levels.
/// All counts default to zero when no advisories exist at that level.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: i64,
    /// Number of advisories with High severity.
    pub high: i64,
    /// Number of advisories with Medium severity.
    pub medium: i64,
    /// Number of advisories with Low severity.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
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

- **`i64` for counts**: Matches the integer types used in sibling model structs and aligns
  with PostgreSQL's `bigint`/`int8` type mapping in SeaORM.
- **`Default` impl**: Provides a zero-initialized instance, useful for the case where an
  SBOM has no linked advisories.
- **`PartialEq, Eq`**: Added for test assertion support (`assert_eq!`).
- **Doc comments on every field**: Required by the skill's code quality practices.
- **Serde derives**: `Serialize` for JSON responses, `Deserialize` for potential use in
  tests or request deserialization.

## Conventions Applied

- Derive macros: `Debug, Clone, Serialize, Deserialize` matching sibling model structs.
- Module-level doc comment (`//!`) describing the module's purpose.
- Struct-level and field-level doc comments using `///`.
- PascalCase for the struct name.
- File named in snake_case matching the struct name.

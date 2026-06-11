# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated severity
counts for advisories linked to a given SBOM. This is the response type for the new
`GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

Create a new file with the following contents:

```rust
//! Severity summary model for advisory aggregation.
//!
//! Provides a response struct that aggregates vulnerability advisory
//! severity counts for a given SBOM.

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Returns the number of unique advisories at each severity level
/// (critical, high, medium, low) plus a total count. All counts
/// default to zero when no advisories exist at that level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: i64,
    /// Number of high-severity advisories.
    pub high: i64,
    /// Number of medium-severity advisories.
    pub medium: i64,
    /// Number of low-severity advisories.
    pub low: i64,
    /// Total number of unique advisories across all severity levels.
    pub total: i64,
}
```

## Conventions Applied

- **Derive macros**: `Clone, Debug, Serialize, Deserialize` matching sibling model structs (`AdvisorySummary`, `SbomSummary`)
- **Default derive**: Added `Default` so all counts initialize to 0, satisfying the acceptance criterion that severity levels default to 0
- **ToSchema derive**: For OpenAPI spec generation (if utoipa is used in the project)
- **Documentation**: Every field has a `///` doc comment per the code quality practices requirement
- **Module-level docs**: `//!` doc comment at the top of the file
- **Field types**: `i64` for counts, consistent with SeaORM integer types used elsewhere
- **Naming**: PascalCase struct name following the pattern of `AdvisorySummary`, `SbomDetails`

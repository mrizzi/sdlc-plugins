# File 4: modules/fundamental/src/advisory/model/severity_summary.rs

## Change Type: Create

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory severity counts for an SBOM. This struct is returned by the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

### Full file content

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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
```

## Conventions Applied

- File name matches struct name in snake_case (`severity_summary.rs` -> `SeveritySummary`)
- Derives follow existing model patterns: `Clone, Debug, Serialize, Deserialize` (observed in sibling structs `SbomSummary`, `AdvisorySummary`)
- Added `Default` derive so all fields default to 0 when no advisories exist (fulfills acceptance criterion)
- Added `ToSchema` derive for OpenAPI/utoipa schema generation (consistent with API model patterns)
- Documentation comments on the struct and each field using `///` convention
- Struct is public (`pub struct`) consistent with sibling models
- Fields are public (`pub`) consistent with sibling model fields
- Uses `u64` for count fields -- appropriate for aggregate counts

## Sibling Parity

Compared against sibling model files:
- `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) -- similar derive set, public fields, doc comments
- `modules/fundamental/src/advisory/model/details.rs` (`AdvisoryDetails`) -- similar structure
- `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) -- similar pattern

The new struct follows the same conventions as all siblings.

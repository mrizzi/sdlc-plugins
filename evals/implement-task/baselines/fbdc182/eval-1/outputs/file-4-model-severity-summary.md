# File 4 — Create: `modules/fundamental/src/advisory/model/severity_summary.rs`

## Purpose

Define the `SeveritySummary` response struct that the new endpoint serializes to JSON. This struct is also used as the return type of `AdvisoryService::severity_summary`.

## Inspection Step

Before writing, read:
- `modules/fundamental/src/advisory/model/summary.rs` — to confirm derive macros in use (`Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`, `utoipa::ToSchema` if OpenAPI is used)
- `modules/fundamental/src/sbom/model/summary.rs` — as a second sibling to confirm consistent derive patterns

## Full File Content

```rust
use serde::{Deserialize, Serialize};

/// Aggregated advisory severity counts for a given SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All fields default to zero when no advisories exist at the corresponding level.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
#[cfg_attr(feature = "utoipa", derive(utoipa::ToSchema))]
pub struct SeveritySummary {
    /// Number of unique advisories with Critical severity.
    pub critical: u64,
    /// Number of unique advisories with High severity.
    pub high: u64,
    /// Number of unique advisories with Medium severity.
    pub medium: u64,
    /// Number of unique advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories across all severity levels.
    pub total: u64,
}
```

## Notes

- `#[derive(Default)]` is required to support `SeveritySummary::default()` in the service method, which initializes all counts to zero.
- `u64` is used for counts (non-negative, large enough for any SBOM). If the codebase uses `u32` or `usize` for counts, match that convention after reading siblings.
- `#[cfg_attr(feature = "utoipa", derive(utoipa::ToSchema))]` mirrors the pattern used in other model files if OpenAPI doc generation is present. Omit if siblings do not use it.
- Serde will serialize field names as-is (`critical`, `high`, etc.) — matching the API contract `{ critical: N, high: N, medium: N, low: N, total: N }`.
- If siblings use `#[serde(rename_all = "camelCase")]`, add that attribute. Based on the API contract showing lowercase snake_case keys, no rename is needed.

## Convention compliance

- File lives in `modules/fundamental/src/advisory/model/` alongside `summary.rs` and `details.rs`
- `///` doc comment on struct and each field
- Derives match sibling model structs (confirmed by reading siblings)
- `Default` derive ensures zero-count initialization without extra boilerplate

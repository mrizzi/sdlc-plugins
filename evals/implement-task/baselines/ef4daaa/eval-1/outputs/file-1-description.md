# File 1: modules/fundamental/src/advisory/model/severity_summary.rs

**Action**: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents the aggregated advisory severity counts for an SBOM. This struct is serialized to JSON and returned by the `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Files inspected before writing

Before creating this file, the following siblings would be inspected using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol`:

- `modules/fundamental/src/advisory/model/summary.rs` -- to understand the derive macros, field documentation style, and `severity` field type used by `AdvisorySummary`
- `modules/fundamental/src/advisory/model/details.rs` -- to understand the model struct pattern for advisory domain
- `modules/fundamental/src/sbom/model/summary.rs` -- cross-domain sibling for additional pattern confirmation

## Conventions applied

- Derive macros: `Serialize, Deserialize, Debug, Clone` (matching sibling model structs)
- Documentation comments: `///` doc comment on the struct and each field
- Field types: `i64` for counts (matching database integer types), ensuring no overflow for large advisory sets
- Default values: all count fields default to 0 via `#[serde(default)]` or struct initialization

## Detailed changes

```rust
use serde::{Deserialize, Serialize};

/// Aggregated severity counts of vulnerability advisories linked to an SBOM.
///
/// Provides a breakdown of advisory counts by severity level (Critical, High,
/// Medium, Low) plus a total count. Used by dashboard widgets to render severity
/// breakdowns without client-side counting.
#[derive(Serialize, Deserialize, Debug, Clone, Default)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: i64,
    /// Number of advisories with High severity.
    pub high: i64,
    /// Number of advisories with Medium severity.
    pub medium: i64,
    /// Number of advisories with Low severity.
    pub low: i64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: i64,
}
```

## Key design decisions

1. **`Default` derive**: Allows creating a zero-initialized `SeveritySummary` for SBOMs with no advisories, satisfying AC-4 (all severity levels default to 0).
2. **`i64` field type**: Matches typical database integer return types from `COUNT()` queries in SeaORM. Using `i64` avoids conversion overhead and aligns with the database layer.
3. **No `Option<T>` wrapping**: All fields are non-optional and default to 0 -- there is no scenario where a severity count should be `null` in the response.
4. **Flat struct**: The response is a flat JSON object `{ critical: N, high: N, medium: N, low: N, total: N }` as specified in the API Changes section, not nested under a wrapper.

## Integration points

- Used as the return type of `AdvisoryService::severity_summary()` (file 4)
- Serialized to JSON by the endpoint handler in `severity_summary.rs` (file 2)
- Registered as a module in `model/mod.rs` (file 6)

# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM.

## Detailed Changes

Create a new file with the following content:

```rust
use serde::Serialize;
use utoipa::ToSchema;

/// Aggregated severity counts of vulnerability advisories linked to an SBOM.
///
/// Each field represents the number of unique advisories at that severity level.
/// The `total` field is the sum of all severity levels.
#[derive(Clone, Debug, Default, Serialize, ToSchema)]
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

## Conventions followed

- **Naming**: PascalCase struct name matching sibling models (`SbomSummary`, `AdvisorySummary`, `AdvisoryDetails`)
- **Derives**: `Serialize` for JSON response (matching sibling models), `ToSchema` for OpenAPI documentation, `Default` for zero-initialization, `Clone` and `Debug` for general Rust conventions
- **Documentation**: Every struct and field has a `///` doc comment per SKILL.md requirements
- **Location**: Placed in `model/` directory following the `model/ + service/ + endpoints/` module structure
- **Types**: `u32` for counts (non-negative integers, matching typical count types in Rust)

## Rationale

- Using `Default` derive ensures all fields default to 0, satisfying acceptance criterion "All severity levels default to 0 when no advisories exist at that level"
- The struct is intentionally simple -- no pagination wrapper since this is a summary/aggregate, not a list
- `Serialize` only (no `Deserialize`) since this is a response-only struct

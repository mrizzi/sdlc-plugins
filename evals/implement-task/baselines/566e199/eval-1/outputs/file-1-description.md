# File 1: modules/fundamental/src/advisory/model/severity_summary.rs (CREATE)

## Purpose
Define the `SeveritySummary` response struct for the advisory severity aggregation endpoint.

## Detailed Changes

Create a new file with the following contents:

### Struct: `SeveritySummary`

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to a specific SBOM.
///
/// Each field represents the count of unique advisories at that severity level.
/// All counts default to zero when no advisories exist at a given level.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema)]
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

### Design decisions

1. **Derive `Default`**: ensures all fields initialize to 0, satisfying the acceptance criterion that severity levels default to 0 when no advisories exist.
2. **Derive `Serialize, Deserialize`**: follows the sibling model pattern from `summary.rs` and `details.rs`.
3. **Derive `ToSchema`**: enables automatic OpenAPI spec generation via utoipa, consistent with other model structs.
4. **`u32` type for counts**: unsigned integer is appropriate for counts that cannot be negative. Matches the expected JSON response shape `{ critical: N, high: N, medium: N, low: N, total: N }`.
5. **Documentation comments**: every field has a `///` doc comment per the code quality practices requirement.

### Conventions followed
- **Derive macros**: matches sibling models (`summary.rs`, `details.rs`) that use `#[derive(Serialize, Deserialize, Debug, Clone)]` plus schema derives.
- **Naming**: struct named `SeveritySummary` follows the `<Concept>Summary` pattern seen in `AdvisorySummary` and `SbomSummary`.
- **File naming**: `severity_summary.rs` follows the lowercase-underscore convention of `summary.rs`, `details.rs`.

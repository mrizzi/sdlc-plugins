# File 1: Create `modules/fundamental/src/advisory/model/severity_summary.rs`

## Action: CREATE

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for an SBOM. This struct is returned by the new endpoint as a JSON response body.

## Detailed Changes

### Imports

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
```

Following the sibling model files (`summary.rs`, `details.rs`), import `Serialize` and `Deserialize` for JSON serialization, and `ToSchema` if the project uses `utoipa` for OpenAPI spec generation.

### Struct Definition

```rust
/// Aggregated advisory severity counts for an SBOM.
///
/// Provides a breakdown of linked advisories by severity level,
/// with a total count. All severity fields default to zero when
/// no advisories exist at that level.
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity.
    pub critical: u64,
    /// Number of advisories with High severity.
    pub high: u64,
    /// Number of advisories with Medium severity.
    pub medium: u64,
    /// Number of advisories with Low severity.
    pub low: u64,
    /// Total number of unique advisories linked to the SBOM.
    pub total: u64,
}
```

### Default Implementation

```rust
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

Alternatively, derive `Default` if all fields are numeric and zero-initialized:

```rust
#[derive(Debug, Clone, Default, Serialize, Deserialize, ToSchema)]
pub struct SeveritySummary { ... }
```

## Conventions Applied

- **Derive macros**: Matches sibling model structs (`Serialize`, `Deserialize`, `Debug`, `Clone`)
- **Documentation**: Every struct and field has a doc comment per the skill's code quality practices
- **Naming**: PascalCase struct name, snake_case fields
- **File location**: Placed in `model/` directory following the domain module pattern
- **No business logic**: Struct is a pure data container, matching sibling model conventions

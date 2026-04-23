# File 1: `modules/fundamental/src/advisory/model/severity_summary.rs` (CREATE)

## Purpose

Define the `SeveritySummary` response struct that represents aggregated advisory severity counts for a given SBOM. This is the data contract returned by the new endpoint.

## Full Contents

```rust
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

/// Aggregated severity counts for advisories linked to an SBOM.
///
/// All counts default to 0 when no advisories exist at that level.
/// The `total` field is the sum of all severity-level counts.
#[derive(Clone, Debug, Default, Serialize, Deserialize, ToSchema, PartialEq, Eq)]
pub struct SeveritySummary {
    /// Number of advisories with Critical severity
    pub critical: u32,
    /// Number of advisories with High severity
    pub high: u32,
    /// Number of advisories with Medium severity
    pub medium: u32,
    /// Number of advisories with Low severity
    pub low: u32,
    /// Total number of unique advisories across all severity levels
    pub total: u32,
}

impl SeveritySummary {
    /// Increment the count for the given severity level string.
    ///
    /// Matches case-insensitively against "critical", "high", "medium", "low".
    /// Advisories with unrecognized or missing severity are still counted in the total.
    pub fn increment(&mut self, severity: &str) {
        match severity.to_lowercase().as_str() {
            "critical" => self.critical += 1,
            "high" => self.high += 1,
            "medium" => self.medium += 1,
            "low" => self.low += 1,
            _ => {} // Unknown severities still counted in total below
        }
        self.total += 1;
    }
}
```

## Design Decisions

1. **`Default` derive**: Ensures all counts start at 0, so an SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }` without special-casing.

2. **`PartialEq, Eq` derives**: Enables easy assertion in tests (`assert_eq!(summary, expected)`).

3. **`ToSchema` derive**: Required for OpenAPI/utoipa documentation generation, consistent with other model structs in the codebase.

4. **`increment` method**: Encapsulates the mapping from severity string to field. This keeps the service method clean and avoids repeating the match logic. The case-insensitive matching is defensive against inconsistent data.

5. **`total` includes all severities**: Even advisories with unrecognized severity values are counted in the total, providing an accurate overall count. The per-level counts may sum to less than total if unknown severities exist.

6. **`u32` type for counts**: Non-negative integers with sufficient range (up to ~4 billion). Advisory counts will never approach this limit.

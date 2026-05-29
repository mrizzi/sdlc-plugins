# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add a `severity_summary` method to the existing `AdvisoryService` that queries advisory severity counts for a given SBOM ID.

## Detailed Changes

### Add method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, following the pattern of the existing `fetch` and `list` methods:

```rust
/// Compute aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts occurrences per severity level.
/// Returns a `SeveritySummary` with all counts (defaulting to zero for absent levels).
///
/// Returns `AppError::NotFound` if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // Use the sbom entity to check existence, following the pattern
    // in existing fetch methods that return NotFound for missing resources.

    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory entity to get severity information
    // Use DISTINCT on advisory ID to deduplicate
    // Group by severity level and count

    // Build SeveritySummary from query results
    // Default all counts to 0, then populate from query results

    // Calculate total as sum of all severity levels

    Ok(summary)
}
```

### Implementation approach

1. **SBOM existence check**: Query the SBOM entity first. If not found, return `Err(AppError::NotFound("SBOM not found".to_string()))` or equivalent, using `.context()` wrapping consistent with the existing `fetch` method pattern.

2. **Advisory severity query**: Use SeaORM to:
   - Select from `sbom_advisory` entity, filtered by `sbom_id`
   - Join to the `advisory` entity to access the severity field
   - Apply `DISTINCT` on advisory ID to satisfy the deduplication criterion
   - Group by severity level
   - Count entries per group

3. **Map results to SeveritySummary**: Initialize a `SeveritySummary::default()` (all zeros), iterate over query results, and set each severity level's count. Compute `total` as the sum.

### Required imports

Add to the file's imports section:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Conventions followed
- **Method signature**: matches `fetch` and `list` -- takes `&self`, entity ID as `Id`, and `tx: &Transactional<'_>`.
- **Return type**: `Result<SeveritySummary, AppError>` -- follows the `Result<T, AppError>` pattern.
- **Error handling**: uses `.context()` wrapping for error messages.
- **Naming**: `severity_summary` follows the `verb_noun` / descriptive-noun pattern.
- **Documentation**: `///` doc comment explaining purpose, parameters, and error behavior.

# File 4: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisory severity counts linked to a given SBOM.

## Detailed Changes

### New method: `severity_summary`

Add a new method to the `impl AdvisoryService` block, following the signature pattern of `fetch` and `list`:

```rust
/// Computes aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates by advisory ID, groups by severity level, and returns
/// the counts. Returns a 404-equivalent error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // First verify the SBOM exists (return 404 if not)
    // Use the SBOM entity to check existence, consistent with other SBOM-scoped endpoints

    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory table to get severity field
    // Use DISTINCT on advisory ID to deduplicate
    // GROUP BY severity level and COUNT

    // Map the query results into SeveritySummary fields:
    // - Match severity strings ("Critical", "High", "Medium", "Low") to struct fields
    // - Default to 0 for any severity level with no advisories
    // - Sum all levels for the total field

    // Return the populated SeveritySummary
}
```

### Implementation approach

1. **SBOM existence check**: Query the SBOM entity first. If not found, return an error that maps to HTTP 404 (matching the pattern used by existing SBOM-scoped endpoints).

2. **Advisory severity query**: Use SeaORM to join `sbom_advisory` with `advisory` entities:
   - Filter by `sbom_id`
   - Select distinct advisory IDs to handle duplicate links
   - Group by the `severity` field from `AdvisorySummary`
   - Count per group

3. **Result mapping**: Convert the query rows into a `SeveritySummary` struct:
   - Initialize with `SeveritySummary::default()` (all zeros)
   - For each (severity, count) row, assign to the matching field
   - Compute `total` as the sum of all counts

### Import additions

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Convention Compliance

- **Method signature**: `&self, entity_id: Id, tx: &Transactional<'_>` matches `fetch` and `list` patterns
- **Error handling**: Returns `Result<T, anyhow::Error>` with `.context()` wrapping on database errors
- **Naming**: `severity_summary` follows the `verb_noun` / descriptive pattern
- **Documentation**: Full doc comment on the method explaining behavior, parameters, and error semantics
- **Database access**: Uses SeaORM queries through the transaction handle, matching sibling methods

# File 3: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

**Purpose**: Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and returns aggregated severity counts.

## Detailed Changes

Add a new method to the `AdvisoryService` impl block. The method follows the pattern of existing `fetch` and `list` methods.

### New method to add

```rust
/// Compute aggregated severity counts for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts occurrences
/// per severity level (Critical, High, Medium, Low).
///
/// Returns a `SeveritySummary` with all counts defaulting to zero when no
/// advisories exist at a given level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (Follow the same pattern used in fetch() for existence checks)

    // Query sbom_advisory join table to get advisory IDs linked to this SBOM
    // Join with advisory table to get severity information
    // Use DISTINCT or collect into HashSet to deduplicate by advisory ID

    // Iterate over unique advisories and count by severity level
    // Use AdvisorySummary.severity field to determine the severity category

    // Build and return SeveritySummary with counts
    // total = critical + high + medium + low

    // Error handling: wrap all database errors with .context()
}
```

### Implementation approach

1. **SBOM existence check**: Query the SBOM entity to verify the ID exists. If not found, return `AppError` with a not-found context, consistent with how other service methods handle missing entities. This satisfies acceptance criterion "Returns 404 when SBOM ID does not exist."

2. **Advisory query**: Use SeaORM to query the `sbom_advisory` join table filtered by `sbom_id`, joining with the advisory table to access severity data. The query should use `DISTINCT` on advisory ID to satisfy acceptance criterion "Counts only unique advisories."

3. **Severity counting**: Initialize a `SeveritySummary::default()` (all zeros). Iterate over query results, matching the severity string (from `AdvisorySummary.severity`) to increment the appropriate counter. Unrecognized severity values are silently skipped (or could be logged as warnings).

4. **Total calculation**: Set `total = critical + high + medium + low` after counting.

5. **Error wrapping**: All fallible operations wrapped with `.context("Failed to compute severity summary for SBOM <id>")`.

### Conventions Applied

- **Method signature**: follows `(&self, entity_id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern from `fetch` and `list`
- **Error handling**: `.context()` wrapping per `common/src/error.rs` pattern
- **Naming**: `severity_summary` follows `verb_noun` / `noun_noun` pattern consistent with existing methods
- **Documentation**: doc comment on the method explaining behavior, parameters, and return value
- **Transaction parameter**: accepts `&Transactional<'_>` for consistency with other service methods

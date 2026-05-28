# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add the `severity_summary` method to the existing `AdvisoryService` struct. This method
queries the database for all advisories linked to a given SBOM, deduplicates by advisory
ID, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

### Add import for the new model

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### Add `severity_summary` method to `AdvisoryService` impl block

Insert the new method inside the existing `impl AdvisoryService { ... }` block,
after the existing `fetch` and `list` methods:

```rust
/// Computes a severity summary for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts advisories by severity level. Returns a
/// `SeveritySummary` with per-level counts and a total.
///
/// Returns `AppError::NotFound` if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // Use existing SBOM lookup pattern -- likely via SbomService or direct entity query
    // If SBOM not found, return Err(AppError::NotFound("SBOM not found".into()))

    // Query sbom_advisory join table for all advisory IDs linked to this SBOM
    // Use SeaORM: entity::sbom_advisory::Entity::find()
    //     .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
    //     .all(tx)

    // Load each advisory's summary to get the severity field
    // Deduplicate by advisory ID using a HashSet<Id>
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for sbom_adv in sbom_advisories {
        if !seen.insert(sbom_adv.advisory_id) {
            continue; // skip duplicate
        }

        // Fetch the AdvisorySummary to access the severity field
        // Match on severity level and increment the appropriate counter
        match advisory_summary.severity.as_deref() {
            Some("Critical") | Some("critical") => summary.critical += 1,
            Some("High") | Some("high") => summary.high += 1,
            Some("Medium") | Some("medium") => summary.medium += 1,
            Some("Low") | Some("low") => summary.low += 1,
            _ => {} // unknown or None severity -- not counted in any bucket
        }
        summary.total += 1;
    }

    Ok(summary)
}
```

### Performance consideration

The implementation above fetches advisory summaries individually (N+1 pattern). For the
performance requirement (under 200ms for 500 advisories), a more efficient approach would
be to use a single SQL query with GROUP BY:

```sql
SELECT a.severity, COUNT(DISTINCT sa.advisory_id) as count
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
GROUP BY a.severity
```

This could be implemented using SeaORM's `select_also` or a raw query, depending on what
patterns exist in the codebase. The choice would be made after inspecting how other service
methods handle similar aggregation queries. If siblings use raw SQL for aggregations, follow
that pattern; if they use SeaORM's query builder, use that instead.

## Conventions followed

- Method signature matches existing patterns: `async fn verb_noun(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Method name follows `verb_noun` convention: `severity_summary`
- Error handling uses `AppError` with contextual messages
- Returns 404 for non-existent SBOM (consistent with existing SBOM endpoints)
- Doc comment on the method explaining behavior, parameters, and error cases
- Placed after existing methods in the impl block (alphabetical or logical ordering)

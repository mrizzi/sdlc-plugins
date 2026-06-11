# File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates vulnerability
advisory severity counts for a given SBOM by querying the `sbom_advisory` join table.

## Detailed Changes

### Add import for the new model

At the top of the file, add the import for `SeveritySummary`:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also ensure the `sbom_advisory` entity import is present (it may already be imported):

```rust
use entity::sbom_advisory;
```

And any necessary SeaORM imports for querying:

```rust
use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect};
```

### Add `severity_summary` method to `AdvisoryService` impl block

Add the following method to the existing `impl AdvisoryService` block, following the
pattern of the existing `fetch` and `list` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts the number of
/// advisories at each severity level (critical, high, medium, low).
///
/// Returns a `SeveritySummary` with all counts defaulting to zero when no
/// advisories exist at a given severity level. Returns an error if the
/// SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Verify the SBOM exists; return 404-equivalent error if not
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| anyhow::anyhow!("SBOM not found"))
        .context("fetching SBOM for severity summary")?;

    // Query advisories linked to this SBOM via the sbom_advisory join table,
    // deduplicating by advisory ID
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx)
        .await
        .context("querying sbom_advisory join table")?;

    // Deduplicate by advisory ID using a HashSet
    let mut seen = std::collections::HashSet::new();
    let unique_advisories: Vec<_> = advisories
        .into_iter()
        .filter(|a| seen.insert(a.advisory_id.clone()))
        .collect();

    // Fetch each unique advisory's summary to get the severity field
    let mut summary = SeveritySummary::default();
    for advisory_link in &unique_advisories {
        if let Some(advisory) = self
            .fetch(advisory_link.advisory_id.clone(), tx)
            .await?
        {
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity — not counted in named buckets
            }
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

**Note**: The exact implementation details (field names on entities, the `severity` field
access path, and how `SbomService` is accessed from `AdvisoryService`) would be confirmed
by inspecting the actual code via Serena before writing. The pattern above follows the
described architecture:

- Method signature matches `fetch`/`list` pattern: `&self, <params>, tx: &Transactional<'_>`
- Error handling uses `.context()` wrapping matching `common/src/error.rs` pattern
- Uses `sbom_advisory` join table as specified in Implementation Notes
- Deduplicates by advisory ID as required by acceptance criteria
- Uses `AdvisorySummary.severity` field for counting as referenced in Implementation Notes

## Conventions Applied

- **Method signature**: follows `verb_noun` naming and takes `&self, id, tx` parameters matching sibling methods
- **Error handling**: uses `anyhow::Error` return type with `.context()` wrapping
- **Database access**: queries via SeaORM entity API using the join table
- **Documentation**: `///` doc comment on the method explaining purpose, behavior, and return semantics
- **Deduplication**: uses `HashSet` for advisory ID deduplication per acceptance criteria

# File 5: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose
Add the `severity_summary` method to `AdvisoryService` that queries advisories linked to a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

### 1. Add import at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### 2. Add the `severity_summary` method to the `impl AdvisoryService` block

Add the following method alongside the existing `fetch`, `list`, and `search` methods:

```rust
/// Returns aggregated severity counts for advisories linked to the given SBOM.
///
/// Deduplicates advisories by ID so that duplicate links are counted only once.
/// Returns 404 if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: &str,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404 if not.
    //    (Use SbomService::fetch or a direct entity query — follow whichever
    //     pattern existing methods use for cross-service lookups.)
    let sbom = sbom::Entity::find_by_id(sbom_id)
        .one(self.db(tx))
        .await?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {sbom_id} not found")))?;

    // 2. Query the sbom_advisory join table for all advisories linked to this SBOM.
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(self.db(tx))
        .await
        .context("querying sbom_advisory join table")?;

    // 3. Collect unique advisory IDs to deduplicate.
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // 4. Fetch the advisory summaries for unique IDs and count by severity.
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        let advisory = advisory::Entity::find_by_id(advisory_id)
            .one(self.db(tx))
            .await
            .context("fetching advisory")?;

        if let Some(adv) = advisory {
            // Map the severity field to the appropriate counter.
            // The exact field name and type depend on the AdvisorySummary/entity
            // struct definition — adapt based on actual severity representation.
            match adv.severity.as_deref() {
                Some("critical") | Some("Critical") => summary.critical += 1,
                Some("high") | Some("High") => summary.high += 1,
                Some("medium") | Some("Medium") => summary.medium += 1,
                Some("low") | Some("Low") => summary.low += 1,
                _ => {} // Unknown or None severity — not counted in any bucket but still in total
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

## Rationale
- Follows the existing service method signature pattern: `&self`, domain identifier, `&Transactional<'_>`, returns `Result<T, AppError>`.
- SBOM existence check returns 404 before proceeding, matching existing SBOM endpoint behavior.
- Deduplication uses `HashSet` on advisory IDs, satisfying the "counts only unique advisories" acceptance criterion.
- All severity fields default to 0 via `SeveritySummary::default()`, satisfying the "defaults to 0" criterion.
- Error handling uses `.context()` wrapping consistent with the project convention.

## Performance Note
For the performance requirement (under 200ms for 500 advisories), the N+1 query pattern above (one query per advisory) may need optimization. A more performant alternative would be a single SQL query with JOIN and GROUP BY:

```rust
// Alternative: single-query approach for better performance
pub async fn severity_summary(
    &self,
    sbom_id: &str,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists
    let _sbom = sbom::Entity::find_by_id(sbom_id)
        .one(self.db(tx))
        .await?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {sbom_id} not found")))?;

    // Single query: join sbom_advisory with advisory, group by severity, count distinct
    let counts: Vec<(String, i64)> = self.db(tx)
        .query_all(Statement::from_sql_and_values(
            DbBackend::Postgres,
            r#"
            SELECT a.severity, COUNT(DISTINCT a.id) as count
            FROM sbom_advisory sa
            JOIN advisory a ON a.id = sa.advisory_id
            WHERE sa.sbom_id = $1
            GROUP BY a.severity
            "#,
            vec![sbom_id.into()],
        ))
        .await
        .context("querying severity counts")?;

    let mut summary = SeveritySummary::default();
    for (severity, count) in counts {
        let c = count as u32;
        match severity.to_lowercase().as_str() {
            "critical" => summary.critical = c,
            "high" => summary.high = c,
            "medium" => summary.medium = c,
            "low" => summary.low = c,
            _ => {}
        }
        summary.total += c;
    }

    Ok(summary)
}
```

The choice between these approaches depends on the project's preference for SeaORM query builder vs raw SQL. The raw SQL approach is O(1) queries and will easily meet the 200ms requirement. The actual implementation should inspect existing service methods to determine which query style the project prefers.

## Exact Types Caveat
The exact entity module paths (`sbom::Entity`, `sbom_advisory::Entity`, `advisory::Entity`), column names, and severity field type (String, enum, or Option) must be confirmed by inspecting:
- `entity/src/sbom_advisory.rs`
- `entity/src/advisory.rs`
- `modules/fundamental/src/advisory/model/summary.rs` (for the `severity` field type)

# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct. This method queries the `sbom_advisory` join table to find all advisories linked to a given SBOM, joins with the advisory table to retrieve severity values, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary` struct.

## Files inspected before writing

Before modifying this file, the following would be inspected:

- `modules/fundamental/src/advisory/service/advisory.rs` -- PRIMARY: `mcp__serena_backend__get_symbols_overview` to see all existing methods, then `mcp__serena_backend__find_symbol("fetch", include_body=true)` and `mcp__serena_backend__find_symbol("list", include_body=true)` to understand the method signature pattern, transactional context usage, query building, and error handling
- `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` -- to verify that adding a new method won't break any existing callers or trait implementations
- `entity/src/sbom_advisory.rs` -- `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure, column definitions, and available SeaORM relations
- `entity/src/advisory.rs` -- `mcp__serena_backend__find_symbol("Model", include_body=true)` to understand the advisory entity and its `severity` field/column
- `modules/fundamental/src/advisory/model/summary.rs` -- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to understand how the `severity` field is typed (String, enum, etc.)
- `modules/fundamental/src/sbom/service/sbom.rs` -- CROSS-DOMAIN SIBLING: to see how SBOM existence is validated in service methods

## Conventions applied

- Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Error wrapping: `.context("...")` pattern from `common/src/error.rs`
- 404 pattern: check SBOM existence first, return `AppError::NotFound` if not found
- Query pattern: use SeaORM query builder with joins and aggregation
- Deduplication: use `DISTINCT` or `GROUP BY advisory_id` in the database query

## Detailed changes

The following method would be added to the `impl AdvisoryService` block, after the existing `list` or `search` method (using `mcp__serena_backend__insert_after_symbol` on the last existing method):

```rust
/// Computes aggregated advisory severity counts for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, groups by severity level, and
/// returns counts for Critical, High, Medium, and Low severities plus a total.
///
/// Returns `AppError::NotFound` if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to look up SBOM")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table,
    // deduplicated by advisory ID
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query advisories for SBOM")?;

    // Deduplicate by advisory ID using a HashSet
    let mut seen_ids = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_advisory, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen_ids.insert(advisory.id.clone()) {
                match advisory.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {} // Unknown or None severity -- not counted in named buckets
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

### Alternative: Database-level aggregation

If performance is a concern for SBOMs with many advisories (AC-5 requires under 200ms for up to 500 advisories), the aggregation could be done entirely in SQL for better performance:

```rust
/// Alternative implementation using raw SQL aggregation for performance.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists (same as above)
    // ...

    // Use raw SQL for efficient aggregation with deduplication
    let results = tx.connection()
        .query_all(Statement::from_sql_and_values(
            DbBackend::Postgres,
            r#"
            SELECT
                COALESCE(a.severity, 'unknown') as severity,
                COUNT(DISTINCT a.id) as count
            FROM sbom_advisory sa
            JOIN advisory a ON sa.advisory_id = a.id
            WHERE sa.sbom_id = $1
            GROUP BY a.severity
            "#,
            [sbom_id.into()],
        ))
        .await
        .context("Failed to aggregate advisory severities")?;

    let mut summary = SeveritySummary::default();
    for row in results {
        let severity: String = row.try_get("", "severity")?;
        let count: i64 = row.try_get("", "count")?;
        match severity.as_str() {
            "critical" => summary.critical = count,
            "high" => summary.high = count,
            "medium" => summary.medium = count,
            "low" => summary.low = count,
            _ => {}
        }
        summary.total += count;
    }

    Ok(summary)
}
```

The choice between ORM-level and SQL-level aggregation would be determined by inspecting what pattern the existing codebase uses. If sibling service methods use raw SQL for aggregation queries, the SQL approach should be followed. If they consistently use the SeaORM query builder, the ORM approach should be used.

## Key design decisions

1. **SBOM existence check**: The method first verifies the SBOM exists, returning 404 if not found. This satisfies AC-2 and is consistent with how other SBOM-scoped endpoints handle non-existent resources.
2. **Deduplication**: Uses `HashSet` (or `COUNT(DISTINCT a.id)` in SQL) to ensure each advisory is counted only once, satisfying AC-3.
3. **Default to zero**: Uses `SeveritySummary::default()` as the starting point, ensuring all severity levels start at 0, satisfying AC-4.
4. **Unknown/null severity handling**: Advisories with unknown or null severity are counted in the `total` but not in any named severity bucket. This is a defensive choice -- if the task requires a different behavior, it would be flagged to the user.
5. **Dependency on SbomService**: The method may need access to a reference to `SbomService` for the SBOM existence check. This would be verified by inspecting how `AdvisoryService` is constructed and whether it already holds a reference to `SbomService`. If not, an alternative approach (direct SBOM entity query) would be used.

## Integration points

- Called by the endpoint handler in `severity_summary.rs` (file 2)
- Returns `SeveritySummary` (file 1)
- Uses `entity::sbom_advisory` join table and `entity::advisory` entity for querying
- Uses `AppError` from `common/src/error.rs` for error handling
- May depend on `SbomService` for SBOM existence validation (would need to verify during implementation)

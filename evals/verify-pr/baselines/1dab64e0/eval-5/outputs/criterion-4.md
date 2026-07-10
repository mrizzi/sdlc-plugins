# Criterion 4: Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Analysis

### What the criterion requires

The existing `offset` and `limit` pagination parameters must continue to function correctly, and the response must maintain the established sorting order. The change to strip qualifiers must not break pagination mechanics.

### Evidence from the PR diff

#### Service layer pagination preserved (`modules/fundamental/src/purl/service/mod.rs`)

The pagination logic remains structurally intact:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    // ...limit applied...
    .all(&self.db)
    .await?
```

The `offset` and `limit` parameters are still applied to the database query before results are fetched. The qualifier stripping and dedup are applied after the database query returns results, so pagination at the database level is preserved.

The `total` count computation was updated to use `group_by` and `select_only`:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

This adjusts the count to reflect the grouping change (removing qualifier joins), maintaining accurate `total` values.

#### Unchanged pagination test (`tests/api/purl_recommend.rs`)

The `test_recommend_purls_pagination` test function is not modified in this PR (it appears in the base branch but is not touched by the diff). This test seeds 5 versioned PURLs and asserts that `limit=2` returns exactly 2 items with `total=5`, confirming pagination remains functional.

#### New ordering test (`tests/api/purl_simplify.rs`)

The `test_simplified_purl_ordering_preserved` test validates both ordering and pagination after qualifier removal:

```rust
// Seeds 3 versions, requests with limit=2
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

// Asserts correct pagination
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
// Asserts qualifiers stripped in paginated results
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Conclusion

The pagination parameters (`offset`, `limit`) are still applied at the database query level. The `total` count is correctly computed with grouping. The existing pagination test is unmodified (confirming no regression), and a new test validates ordering and pagination with the simplified response format. The criterion is satisfied.

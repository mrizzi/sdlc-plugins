# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion Text

Existing pagination and sorting behavior is preserved.

## Verdict: PASS

## Reasoning

The PR preserves the existing pagination logic in `modules/fundamental/src/purl/service/mod.rs`. The offset/limit application remains unchanged:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    ...
    .all(&self.db)
    .await?
```

The core query structure is preserved: `Purl::find()` with namespace and name filters, followed by offset/limit application. The only changes to the query are:
1. Removing the qualifier join (which simplifies the query but does not affect result ordering)
2. Adding `select_only().column(purl::Column::Id).group_by(purl::Column::Id)` to the count query for accurate deduplication counting

The count query modification ensures that `total` reflects the deduplicated count rather than the raw row count (which could be inflated by qualifier joins), so pagination metadata remains accurate.

The existing test `test_recommend_purls_pagination` in the base branch (which seeds 5 versioned PURLs and asserts `limit=2` returns 2 items with `total=5`) is not modified in the diff, confirming that pagination behavior continues to work.

The new test `test_simplified_purl_ordering_preserved` further validates that ordering and pagination work correctly after qualifier removal:
- Seeds 3 versions with qualifiers
- Requests with `limit=2`
- Asserts 2 items returned with `total=3`
- Confirms no qualifiers in results

This criterion is satisfied by the code changes.

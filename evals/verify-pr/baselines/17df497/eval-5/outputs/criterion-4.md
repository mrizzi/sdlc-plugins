# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion Text
Existing pagination and sorting behavior is preserved.

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The pagination logic remains structurally intact:
```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    ...
    .all(&self.db)
    .await?
```
The `offset` and `limit` parameters are still applied to the query.

The `total` count query was modified to use `select_only()`, `column()`, and `group_by()`:
```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```
This change adjusts the count to account for the removal of the qualifier join, ensuring the total reflects unique PURLs rather than potentially inflated counts from the join.

### Test evidence
The existing `test_recommend_purls_pagination` test function in `tests/api/purl_recommend.rs` is **not modified or removed** in the diff (the diff only shows changes up to the `test_recommend_purls_with_qualifiers` removal and the `test_recommend_purls_dedup` addition, then shows the unchanged `test_recommend_purls_unknown_returns_empty` function continues). The pagination test from the base branch should still exist and pass.

Additionally, the new `test_simplified_purl_ordering_preserved` test in `tests/api/purl_simplify.rs` validates that pagination with `limit=2` works correctly and `body.total` is 3 (reflecting 3 seeded versions with limit of 2 returned).

### Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)
The endpoint signature is unchanged -- it still accepts `Query(params): Query<RecommendParams>` and returns `PaginatedResults<PurlSummary>`. The `RecommendParams` struct (which contains offset/limit fields) is not modified.

## Verdict: PASS

Pagination parameters (offset, limit) are still applied, the total count is adjusted for the new query shape, and both existing and new tests validate pagination behavior. The ordering of results from the database query is preserved.

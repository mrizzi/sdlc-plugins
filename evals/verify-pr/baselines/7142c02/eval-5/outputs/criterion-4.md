# Criterion 4: Pagination and sorting behavior preserved

**Acceptance Criterion:** Existing pagination and sorting behavior is preserved

**Verdict: PASS**

## Evidence

### Production code changes

The pagination logic in `modules/fundamental/src/purl/service/mod.rs` is preserved. The query still uses:

```rust
.offset(offset.unwrap_or(0) as u64)
```

and the `limit` parameter (applied via `.limit()`). The `total` count calculation was adjusted to use `select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()` to account for the removed qualifier join, but the pagination mechanism itself (offset, limit, total count in response) remains unchanged.

The response structure `PaginatedResults { items, total }` is still used identically.

### Test coverage

The existing `test_recommend_purls_pagination` test in the base branch was **not modified** in this PR -- it is absent from the diff, meaning it remains unchanged. This test seeds 5 versioned PURLs and asserts that `limit=2` returns 2 items with `total=5`, confirming pagination continues to work.

Additionally, the new `test_simplified_purl_ordering_preserved` function in `tests/api/purl_simplify.rs` verifies that ordering and pagination work together after qualifier removal:

```rust
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

### Conclusion

Pagination parameters (offset, limit) continue to be applied, the total count is correctly computed, and both existing and new tests validate pagination behavior. This criterion is satisfied.

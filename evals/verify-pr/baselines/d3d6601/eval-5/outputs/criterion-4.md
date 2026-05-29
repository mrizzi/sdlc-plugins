# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion Text
Existing pagination and sorting behavior is preserved.

## Verdict: PASS

## Reasoning

The pagination mechanism in `modules/fundamental/src/purl/service/mod.rs` is preserved. The PR retains the existing `offset` and `limit` application:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    ...
    .all(&self.db)
    .await?
```

The `total` count computation is modified slightly to use `select_only()`, `column()`, and `group_by()` instead of a simple `.count()`, but this is a refinement to support correct counting after qualifier join removal, not a change to pagination behavior.

The existing pagination test `test_recommend_purls_pagination` in the base-branch version of `tests/api/purl_recommend.rs` is preserved in the PR (it appears in the diff as unchanged context). This test verifies that `limit=2` returns only 2 items while `total` reflects all 5 versions.

Additionally, the new test `test_simplified_purl_ordering_preserved` in `tests/api/purl_simplify.rs` explicitly tests pagination with the simplified format:

```rust
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

This confirms that pagination parameters (`limit`) work correctly with the simplified response format, and that ordering is preserved.

The `RecommendParams` struct in the endpoint handler (`recommend.rs`) is unchanged, continuing to accept `offset` and `limit` query parameters.

This criterion is satisfied.

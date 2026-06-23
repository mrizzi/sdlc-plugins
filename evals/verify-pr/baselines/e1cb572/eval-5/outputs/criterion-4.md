# Criterion 4: Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Reasoning

The PR preserves the existing pagination parameters (`offset` and `limit`) in the service layer query. In `modules/fundamental/src/purl/service/mod.rs`, the query continues to apply offset and limit to the database query, maintaining the same pagination interface for API consumers.

The test `test_simplified_purl_ordering_preserved` in the new file `tests/api/purl_simplify.rs` explicitly verifies pagination behavior post-change:

```rust
// Given 3 versioned PURLs
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

// When requesting with limit=2
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

// Then pagination works correctly
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

Additionally, the existing test `test_recommend_purls_pagination` in `tests/api/purl_recommend.rs` (unchanged from the base branch) continues to verify pagination with 5 seeded PURLs and `limit=2`, asserting `items.len() == 2` and `total == 5`. This test's continued passing (CI passes) confirms backward-compatible pagination behavior.

The total count computation was updated to use `select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()`, but this produces the same result since each PURL row has a unique ID. The `total` field in `PaginatedResults` continues to reflect the full count of matching results.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `offset` and `limit` application unchanged
- `tests/api/purl_simplify.rs`: `test_simplified_purl_ordering_preserved` verifies `limit=2` returns 2 items with `total=3`
- `tests/api/purl_recommend.rs`: Existing `test_recommend_purls_pagination` unchanged and passing
- CI: All checks pass

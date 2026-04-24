# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion
Existing pagination and sorting behavior is preserved.

## Result: PASS

## Detailed Reasoning

### Pagination Implementation

In `modules/fundamental/src/purl/service/mod.rs`, the pagination logic remains intact in the PR:

```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    // ... limit applied
    .all(&self.db)
    .await?
```

The `offset` and `limit` parameters are still passed through from the endpoint handler. The endpoint signature in `recommend.rs` still accepts `Query(params): Query<RecommendParams>` which includes `offset` and `limit` fields.

### Total Count

The total count query is preserved but modified to use `group_by` for correctness after removing the qualifier join:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

Previously the total was computed as `query.clone().count(&self.db).await?` with the qualifier join included. The new version uses `group_by` and `select_only` to ensure accurate counting after the join removal. The `total` field is still included in the `PaginatedResults` response.

### Test Verification

The existing `test_recommend_purls_pagination` test from the base branch (which is NOT modified in this PR) continues to verify pagination behavior. This test seeds 5 PURLs, requests with `limit=2`, and asserts `body.items.len() == 2` and `body.total == 5`. Since this test is not modified and CI passes (as stated in the task), pagination behavior is preserved.

Additionally, the new `test_simplified_purl_ordering_preserved` test in `purl_simplify.rs` explicitly verifies pagination with qualifier removal:

```rust
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

This confirms that `limit` is applied correctly and `total` reflects the full count, even after qualifier removal.

### Sorting

The query does not explicitly modify sorting behavior. The base query ordering is preserved. The diff does not touch any `order_by` clauses, so sorting behavior remains unchanged from the base branch.

The criterion is satisfied -- pagination parameters (offset, limit, total count) continue to work correctly.

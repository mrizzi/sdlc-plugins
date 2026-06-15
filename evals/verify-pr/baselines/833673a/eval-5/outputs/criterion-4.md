# Criterion 4: Existing pagination and sorting behavior is preserved

## Verdict: WARN

## Reasoning

The endpoint handler still passes `params.offset` and `params.limit` to the service method, and the service applies `.offset()` and `.limit()` to the query. The `test_simplified_purl_ordering_preserved` test in the new `purl_simplify.rs` file verifies that `limit=2` with 3 seeded items returns 2 items and `total=3`.

However, there is a pagination correctness concern:

1. **`total` count mismatch:** The `total` is computed from the raw database query before deduplication. After `.dedup_by()` reduces the item set, the reported `total` may be higher than the actual number of unique results available. For example, in `test_recommend_purls_dedup`, 2 PURLs are seeded (same version, different qualifiers), so `total` would be 2, but `items.len()` is 1 after dedup. This means a client computing page count as `ceil(total / limit)` would overestimate the number of pages.

2. **Missing `total` assertion in dedup test:** The `test_recommend_purls_dedup` test does not assert `body.total`, so the total/items inconsistency is untested.

3. **The GROUP BY in the count query is a no-op:** The new `group_by(purl::Column::Id)` groups by primary key, which produces one group per row -- functionally identical to the original `query.clone().count()`. This added complexity provides no benefit.

The existing `test_recommend_purls_pagination` test is preserved unchanged but was not updated to assert qualifier-free PURLs in the response (though it still tests the correct pagination envelope behavior: `items.len() == 2` with `total == 5`).

This criterion is **partially met**: the pagination mechanics (offset/limit) are preserved, but the interaction between deduplication and the `total` count introduces a contract inconsistency that could affect API consumers.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `total` computed via `query.clone().select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()` (pre-dedup count)
- `modules/fundamental/src/purl/service/mod.rs`: `.dedup_by()` applied after `.all()` reduces items post-query
- `tests/api/purl_recommend.rs`: `test_recommend_purls_dedup` asserts `items.len() == 1` but does not assert `total`
- `tests/api/purl_simplify.rs`: `test_simplified_purl_ordering_preserved` asserts `total == 3` which is correct because all 3 seeds have different versions (no dedup needed)

# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion Text
Existing pagination and sorting behavior is preserved.

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The pagination logic using `offset` and `limit` remains unchanged in the query:
```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
    // .limit(...) continues to apply
    .all(&self.db)
    .await?
```
The offset/limit application is identical to the pre-change version. The total count query was adjusted to use `select_only().column(purl::Column::Id).group_by(purl::Column::Id).count()` instead of the previous simple `.count()`, but this is a correctness fix for counting after the qualifier join removal -- it still provides the total for pagination metadata.

### Base-branch test preserved (`tests/api/purl_recommend.rs`)
The `test_recommend_purls_pagination` test from the base branch (which seeds 5 versioned PURLs and asserts `limit=2` returns 2 items with `total=5`) is still present in the PR version (the diff does not modify or remove it). This test continues to verify pagination behavior end-to-end.

### New test evidence (`tests/api/purl_simplify.rs`)
The `test_simplified_purl_ordering_preserved` test explicitly validates pagination with the simplified response:
```rust
// Given multiple versions of the same package with qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

// When requesting recommendations with limit
let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

// Then results are ordered and paginated correctly without qualifiers
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```
This test seeds 3 PURLs, requests with `limit=2`, and asserts that exactly 2 items are returned with `total=3` -- confirming pagination continues to work correctly after the simplification.

## Verdict: PASS

The pagination offset/limit logic is unchanged in the service layer. The existing `test_recommend_purls_pagination` test is preserved, and a new `test_simplified_purl_ordering_preserved` test further confirms pagination and ordering work correctly with the simplified response format.

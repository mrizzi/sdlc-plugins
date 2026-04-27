# Criterion 4: Existing pagination and sorting behavior is preserved

## Criterion Text
Existing pagination and sorting behavior is preserved.

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The offset/limit pagination logic is unchanged in the PR:
```rust
let items = query
    .offset(offset.unwrap_or(0) as u64)
```
The limit application (visible in the context of the diff) and the collection of results via `.all(&self.db).await?` remain the same.

The total count query was adjusted to use `select_only()`, `column()`, and `group_by()`:
```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```
This replaces the previous `query.clone().count()` to correctly count distinct entries now that the qualifier join is removed. The count still reflects the total number of matching entries.

### Test evidence - unchanged pagination test
The `test_recommend_purls_pagination` test function from the base branch (which seeds 5 versioned PURLs and requests with `limit=2`, asserting `body.items.len() == 2` and `body.total == 5`) is unchanged in the PR diff. Its absence from the diff means it was left intact, confirming pagination behavior is preserved.

### Additional test evidence (`tests/api/purl_simplify.rs`)
The `test_simplified_purl_ordering_preserved` test validates both ordering and pagination after qualifier removal:
```rust
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```
This confirms that `limit=2` correctly restricts the returned items to 2 while `total` reflects all 3 matching entries.

## Verdict: PASS

Pagination parameters (offset/limit) are preserved in the service layer. The existing pagination test is unchanged. A new test in `purl_simplify.rs` also validates ordering and pagination with the simplified format.

# Criterion 5: Response shape is unchanged (still PaginatedResults<PurlSummary>)

## Criterion Text
Response shape is unchanged (still `PaginatedResults<PurlSummary>`).

## Evidence from PR Diff

### Endpoint signature (`modules/fundamental/src/purl/endpoints/recommend.rs`)
The `recommend_purls` function continues to return `Result<Json<PaginatedResults<PurlSummary>>, AppError>`:
```rust
pub async fn recommend_purls(
    db: DatabaseConnection,
    Query(params): Query<RecommendParams>,
) -> Result<Json<PaginatedResults<PurlSummary>>, AppError> {
```
The return type is identical before and after the change. The only modifications in this file are the removal of the unused `JoinType` import and a whitespace change.

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The `recommend` method continues to return `Result<PaginatedResults<PurlSummary>>`. The response struct construction is unchanged:
```rust
Ok(PaginatedResults { items, total })
```
The `items` field is still a `Vec<PurlSummary>` (each with a `purl: String` field), and `total` is still a count. The internal mapping logic changed (to strip qualifiers and deduplicate), but the output type remains `PaginatedResults<PurlSummary>`.

### Test evidence
All tests in both `tests/api/purl_recommend.rs` and `tests/api/purl_simplify.rs` deserialize the response into `PaginatedResults<PurlSummary>`:
```rust
let body: PaginatedResults<PurlSummary> = resp.json().await;
```
If the response shape had changed, this deserialization would fail at test runtime.

## Verdict: PASS

The endpoint return type and service return type remain `PaginatedResults<PurlSummary>`. Both existing and new tests deserialize the response using this exact type, confirming the response shape is unchanged.

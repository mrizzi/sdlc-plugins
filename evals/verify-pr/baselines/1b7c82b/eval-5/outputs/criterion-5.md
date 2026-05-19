# Criterion 5: Response shape is unchanged (PaginatedResults<PurlSummary>)

## Criterion Text
Response shape is unchanged (still `PaginatedResults<PurlSummary>`)

## Verdict: PASS

## Reasoning

### Code evidence

The endpoint handler in `modules/fundamental/src/purl/endpoints/recommend.rs` continues to return `Result<Json<PaginatedResults<PurlSummary>>, AppError>`. The return type signature was not changed in the PR diff -- only the `JoinType` import was removed and minor whitespace changes were made. The handler still wraps the service result in `Json()`.

The service method in `modules/fundamental/src/purl/service/mod.rs` still constructs and returns `PaginatedResults { items, total }`:

```rust
Ok(PaginatedResults { items, total })
```

The `items` vector still contains `PurlSummary` structs:

```rust
PurlSummary {
    purl: simplified.to_string(),
}
```

The only change is the value of the `purl` field (now a simplified PURL string without qualifiers), not the structure of the response. The `PurlSummary` struct still has a `purl` field of type `String`, and `PaginatedResults` still wraps a `Vec<PurlSummary>` with a `total` count.

### Test evidence

All tests in both `tests/api/purl_recommend.rs` and `tests/api/purl_simplify.rs` deserialize the response as `PaginatedResults<PurlSummary>`:

```rust
let body: PaginatedResults<PurlSummary> = resp.json().await;
```

This deserialization would fail at runtime if the response shape had changed. The fact that all tests use the same response type confirms the shape is preserved.

Additionally, all tests access `body.items` (the paginated item list) and individual `body.items[N].purl` fields, confirming the internal structure of `PurlSummary` is unchanged. The `test_recommend_purls_dedup` and `test_simplified_purl_ordering_preserved` tests also access `body.total`, confirming the total count field remains present.

The response shape is fully preserved -- the only semantic change is the content of the PURL strings within the unchanged structure.

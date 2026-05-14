# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Result:** PASS

## Evidence

### Implementation changes

In `modules/fundamental/src/purl/service/mod.rs`, the PR introduces qualifier stripping in the recommendation service:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This replaces the previous implementation that serialized the full PURL including qualifiers:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The `without_qualifiers()` method is called on each PURL before converting to string, which strips all qualifier key-value pairs from the response.

### Endpoint changes

In `modules/fundamental/src/purl/endpoints/recommend.rs`, the `JoinType` import for qualifier joins was removed, confirming the endpoint no longer joins qualifier data:

```diff
-use sea_orm::JoinType;
```

### Test confirmation

The updated `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` asserts the new behavior:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the response now returns versioned PURLs (with `@3.12` version) but without qualifiers (no `?repository_url=...&type=jar`).

### Reasoning

The implementation changes in the service layer use `without_qualifiers()` to strip qualifiers, the endpoint removes the qualifier join, and the test asserts on a versioned PURL without qualifier parameters. This criterion is satisfied.

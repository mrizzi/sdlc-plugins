# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text

> `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Detailed Reasoning

### Code Changes Examined

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The core change is in the `recommend` method of `PurlService`. The diff shows that after fetching results from the database, the code now calls `p.without_qualifiers()` before serializing to string:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code mapped directly:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The `without_qualifiers()` method is documented in the task's Implementation Notes as being available on the `PackageUrl` builder in `common/src/purl.rs`. This method strips all qualifier key-value pairs from the PURL, leaving only the type, namespace, name, and version components.

**Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The qualifier join import (`use sea_orm::JoinType;`) was removed, confirming the endpoint no longer depends on qualifier data. The endpoint still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, meaning the response structure is unchanged.

**Test confirmation (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the response contains a versioned PURL (`@3.12`) without any qualifier suffix. The previous assertion checked for the full qualified PURL with `?repository_url=...&type=jar`.

### Conclusion

The combination of `without_qualifiers()` in the service layer and the updated test assertion directly demonstrates that the endpoint returns versioned PURLs without qualifiers. The acceptance criterion is satisfied.

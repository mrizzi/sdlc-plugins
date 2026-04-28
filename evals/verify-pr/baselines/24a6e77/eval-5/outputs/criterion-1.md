# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

This criterion requires that the recommendation endpoint returns versioned PURLs (e.g., `pkg:maven/org.apache/commons-lang3@3.12`) rather than fully qualified PURLs with qualifiers (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`).

### Code changes supporting this criterion

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The PR modifies the `recommend` method to strip qualifiers from PURLs before returning them. The key change is:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Previously, the code used `p.to_string()` directly, which would include qualifiers. Now it calls `p.without_qualifiers()` first, which produces a versioned PURL without the query parameter portion.

**Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`):**

The `JoinType` import was removed since the qualifier join is no longer needed. The endpoint still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, preserving the response shape.

**Test verification (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test now asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns a versioned PURL without qualifiers. The test seeds PURLs with qualifiers (`?repository_url=...&type=jar`) but expects the response to contain only the versioned form.

### Conclusion

The code changes in the service layer explicitly strip qualifiers using `without_qualifiers()`, and the test validates that the response contains versioned PURLs without qualifier query parameters. This criterion is satisfied.

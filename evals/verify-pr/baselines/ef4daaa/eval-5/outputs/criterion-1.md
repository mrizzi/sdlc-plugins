# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text
> GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3 returns versioned PURLs without qualifiers

## Verdict: PASS

## Detailed Reasoning

### Service Layer Changes

The diff in `modules/fundamental/src/purl/service/mod.rs` shows the critical change that implements this criterion. The previous code mapped query results directly:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

The new code calls `without_qualifiers()` before serialization:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

This uses the existing `PackageUrl` builder's `without_qualifiers()` method as specified in the Implementation Notes of the task description. The `without_qualifiers()` method strips all qualifier key-value pairs (everything after `?` in the PURL string), returning only the scheme, type, namespace, name, and version components.

### Endpoint Layer Changes

The diff in `modules/fundamental/src/purl/endpoints/recommend.rs` shows two changes:
1. Removed the `use sea_orm::JoinType;` import (no longer needed since qualifier joins are removed)
2. The handler function continues to return `Result<Json<PaginatedResults<PurlSummary>>, AppError>`, preserving the response shape

The handler still calls `PurlService::new(&db).recommend(...)` which now returns simplified PURLs.

### Query Layer Changes

The service layer also removes the qualifier join from the query:

```diff
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
+            .filter(purl::Column::Name.eq(&base_purl.name));
```

This means qualifier data is no longer fetched from the database at all, which is consistent with not including qualifiers in the response.

### Test Evidence

The updated `test_recommend_purls_basic` test directly verifies this criterion:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This assertion confirms the response contains a versioned PURL (`@3.12` version present) without qualifiers (no `?repository_url=...&type=...` suffix).

The new `purl_simplify.rs` file adds additional edge case coverage confirming versioned PURLs without qualifiers across different PURL types (npm, pypi).

### Conclusion

The code changes implement this criterion completely. The service layer strips qualifiers using `without_qualifiers()`, the query layer no longer joins qualifier tables, and multiple tests verify the expected output format.

# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text

> Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Detailed Reasoning

### Code Changes Examined

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The `without_qualifiers()` call strips all qualifier key-value pairs. In PURL format, qualifiers appear after a `?` character (e.g., `pkg:maven/org/name@1.0?repository_url=...&type=jar`). By calling `without_qualifiers()`, the resulting PURL string will not contain the `?` separator or any qualifier data after it.

Additionally, the qualifier join was removed from the database query:

```diff
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

This means qualifier data is no longer fetched from the database at all, providing a secondary guarantee that qualifiers cannot leak into the response.

**Test assertions (`tests/api/purl_recommend.rs`):**

The `test_recommend_purls_basic` test explicitly asserts the absence of `?` in response PURLs:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

This is a direct character-level check that no qualifier separator exists in any returned PURL string.

**Additional test coverage (`tests/api/purl_simplify.rs`):**

The new `test_simplified_purl_no_version` test also asserts:

```rust
assert!(!body.items[0].purl.contains('?'));
```

And `test_simplified_purl_mixed_types` asserts:

```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

These additional tests confirm the absence of qualifiers across different PURL types and edge cases.

### Conclusion

The code removes qualifier data at both the database query level (no qualifier join) and the serialization level (`without_qualifiers()`). Tests explicitly assert the absence of the `?` character. The acceptance criterion is satisfied.

# Criterion 2: Response PURLs do not contain `?` query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Result:** PASS

## Evidence

### Implementation changes

In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` call ensures no qualifier parameters appear in the serialized PURL:

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

Additionally, the qualifier join was removed from the query:

```diff
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

This means qualifiers are neither fetched from the database nor included in the response.

### Test confirmation

Multiple test assertions explicitly verify the absence of `?` in response PURLs:

In `test_recommend_purls_basic` (`tests/api/purl_recommend.rs`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version` (`tests/api/purl_simplify.rs`):
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `test_simplified_purl_ordering_preserved` (`tests/api/purl_simplify.rs`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_mixed_types` (`tests/api/purl_simplify.rs`):
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

### Reasoning

The implementation removes qualifier data at both the query level (no join) and the serialization level (`without_qualifiers()`). Multiple tests across two test files explicitly assert that response PURLs do not contain `?` characters. This criterion is satisfied.

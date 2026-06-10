# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

This criterion requires that no PURL in the response contains the `?` character, which would indicate the presence of query parameters (qualifiers).

### Code Implementation

The service layer (`modules/fundamental/src/purl/service/mod.rs`) ensures this through:

1. **`without_qualifiers()` call**: Every PURL model object is passed through `p.without_qualifiers()` before being serialized to a string. According to the task's Implementation Notes, the `PackageUrl` builder in `common/src/purl.rs` supports constructing PURLs with or without qualifiers. The `without_qualifiers()` method strips all qualifier key-value pairs, which are the components that appear after the `?` in a PURL.

2. **Qualifier join removed**: The query no longer joins the `PurlQualifier` relation, so qualifier data is not even fetched from the database. This is a defense-in-depth measure -- even if `without_qualifiers()` were not called, the qualifier data would not be available for serialization.

### Test Evidence

Multiple tests explicitly assert that the `?` character is absent from response PURLs:

**In `tests/api/purl_recommend.rs`:**
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```
These assertions are added to `test_recommend_purls_basic`, directly verifying no qualifiers are present.

**In `tests/api/purl_simplify.rs`:**
```rust
// test_simplified_purl_no_version
assert!(!body.items[0].purl.contains('?'));

// test_simplified_purl_mixed_types
assert!(!body.items[0].purl.contains("vcs_url"));

// test_simplified_purl_ordering_preserved
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These tests cover multiple scenarios (no version, mixed PURL types, ordering with pagination) and all verify the absence of `?` or qualifier-specific content.

### Comprehensiveness

The tests seed PURLs that originally have qualifiers (e.g., `?repository_url=...&type=jar`, `?vcs_url=...`) and verify the response strips them. This proves the behavior works for various qualifier types, not just one specific qualifier pattern.

## Conclusion

Both the implementation (stripping qualifiers via `without_qualifiers()` and removing the qualifier join) and the tests (explicit `contains('?')` assertions across multiple test functions) confirm that response PURLs will not contain `?` query parameters.

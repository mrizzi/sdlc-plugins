# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

This criterion requires that no PURL in the response contains a `?` character, which would indicate the presence of qualifier query parameters.

### Code changes supporting this criterion

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The `without_qualifiers()` method is called on every PURL before it is serialized to a string. The `PackageUrl` builder in `common/src/purl.rs` (referenced in the task's Implementation Notes) supports constructing PURLs with or without qualifiers. By calling `without_qualifiers()`, the resulting string representation will not include the `?` separator or any query parameters.

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

**Query layer change:**

The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) has been removed from the query in the service layer. This means qualifier data is no longer fetched from the database at all, and even if `to_string()` were called on the raw entity, qualifiers would not be populated.

**Test verification:**

Multiple tests explicitly assert the absence of `?` in response PURLs:

In `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `test_simplified_purl_no_version` (new file):
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `test_simplified_purl_mixed_types` (new file):
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `test_simplified_purl_ordering_preserved` (new file):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Conclusion

The implementation strips qualifiers at the service layer and removes the qualifier join from the query. Multiple tests across two test files explicitly assert that no `?` character appears in response PURLs. This criterion is satisfied.

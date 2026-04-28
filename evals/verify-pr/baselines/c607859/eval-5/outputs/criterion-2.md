# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR ensures that no qualifier query parameters appear in the response PURLs through both code logic and test assertions.

### Evidence from the diff

**Service layer (`modules/fundamental/src/purl/service/mod.rs`):**

The `without_qualifiers()` method is called on each PURL before serialization:
```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

The `without_qualifiers()` method (documented in Implementation Notes as being from `common/src/purl.rs`) constructs a PURL without qualifier components, which means no `?` separator and no key=value pairs will appear in the serialized string.

**Test assertions (`tests/api/purl_recommend.rs`):**

The updated `test_recommend_purls_basic` explicitly checks for absence of `?`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

**Additional test assertions (`tests/api/purl_simplify.rs`):**

Multiple tests in the new file also assert qualifier absence:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

### Conclusion

The code strips qualifiers via `without_qualifiers()` before serialization, and multiple tests explicitly assert the absence of `?` in response PURLs. This criterion is satisfied.

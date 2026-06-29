# Criterion 2: No qualifier query parameters in response PURLs

**Acceptance Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## Evidence

### Production code changes

The `without_qualifiers()` call in `modules/fundamental/src/purl/service/mod.rs` strips all qualifier key-value pairs from the PURL. Since qualifiers in the PURL spec are encoded after a `?` character, removing qualifiers means the `?` and everything after it is no longer present in the serialized string.

### Test coverage

In `tests/api/purl_recommend.rs`, the modified `test_recommend_purls_basic` test includes explicit assertions that no `?` character is present in any response PURL:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

Additionally, the new test file `tests/api/purl_simplify.rs` contains similar assertions across multiple test functions:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks a specific qualifier key is absent)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?')); assert!(!body.items[1].purl.contains('?'));`

### Conclusion

Both the production code transformation and multiple test assertions confirm that response PURLs never contain `?` query parameters. This criterion is satisfied.

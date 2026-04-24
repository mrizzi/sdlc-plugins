# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The `without_qualifiers()` method is called on every PURL before serialization, which by definition strips the `?` and all subsequent qualifier key-value pairs.

### Test assertions (`tests/api/purl_recommend.rs`)
The updated `test_recommend_purls_basic` explicitly asserts the absence of `?`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Additional test coverage (`tests/api/purl_simplify.rs`)
The new test file reinforces this criterion with multiple tests:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

## Verdict: PASS

Both the implementation (calling `without_qualifiers()`) and the tests (asserting no `?` in PURLs) confirm this criterion is met.

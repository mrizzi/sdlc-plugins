# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Evidence from PR Diff

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)
The `without_qualifiers()` method is called on every PURL before serialization:
```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```
This method (referenced in the task as existing in `common/src/purl.rs`) removes all qualifier key-value pairs from the PURL, which eliminates the `?` separator and everything after it.

### Test evidence (`tests/api/purl_recommend.rs`)
The updated `test_recommend_purls_basic` test explicitly asserts the absence of `?` in both returned PURLs:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Additional test evidence (`tests/api/purl_simplify.rs`)
Multiple tests in the new file also assert no `?` is present:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

## Verdict: PASS

The `without_qualifiers()` method removes qualifiers (and thus the `?` separator), and multiple test assertions across two test files explicitly verify that no `?` appears in response PURLs.

# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Verdict: PASS

## Reasoning

The implementation uses the `without_qualifiers()` method on each PURL before serialization in the service layer (`modules/fundamental/src/purl/service/mod.rs`):

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

The `without_qualifiers()` method (documented in the task's Implementation Notes as part of `common/src/purl.rs`) constructs a PURL without any qualifier parameters, which means the resulting string will not contain a `?` character.

This behavior is explicitly tested in both test files:

1. In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic` asserts:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. In `tests/api/purl_simplify.rs`, multiple tests assert the absence of `?`:
   - `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
   - `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
   - `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The combination of the `without_qualifiers()` call in the service layer and explicit test assertions for the absence of `?` confirms this criterion is satisfied.

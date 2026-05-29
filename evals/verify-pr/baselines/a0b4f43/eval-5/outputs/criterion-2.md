# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR implements qualifier removal at the service layer in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method on the `PackageUrl` builder (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) strips all qualifier key-value pairs from the PURL representation. Since qualifiers are the component after `?` in a PURL string, calling `without_qualifiers()` followed by `to_string()` produces a PURL with no `?` character.

Test evidence confirms this across multiple test files:

1. **`tests/api/purl_recommend.rs` -- `test_recommend_purls_basic`**:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. **`tests/api/purl_simplify.rs` -- `test_simplified_purl_no_version`**:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. **`tests/api/purl_simplify.rs` -- `test_simplified_purl_mixed_types`**:
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```
   This verifies specific qualifier keys are absent from the response.

4. **`tests/api/purl_simplify.rs` -- `test_simplified_purl_ordering_preserved`**:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

The no-`?` assertion is consistently applied across both the modified and new test files, confirming comprehensive coverage of this criterion.

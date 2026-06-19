# Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The `without_qualifiers()` method is called on every PURL model before serialization, which removes all qualifier key-value pairs. Since qualifiers are appended to PURLs using the `?` character as a separator (e.g., `pkg:maven/org.apache/commons-lang3@3.12?repository_url=...`), stripping qualifiers guarantees that no `?` character appears in the response PURL strings.

### Code evidence

In `modules/fundamental/src/purl/service/mod.rs`:
```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

The `without_qualifiers()` method (pre-existing on the `PackageUrl` builder in `common/src/purl.rs` per the task description) produces a PURL without qualifier components. Since CI passes, this method compiles and produces the expected output.

### Test evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

1. `tests/api/purl_recommend.rs` - `test_recommend_purls_basic`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. `tests/api/purl_simplify.rs` - `test_simplified_purl_no_version`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. `tests/api/purl_simplify.rs` - `test_simplified_purl_mixed_types`:
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```

4. `tests/api/purl_simplify.rs` - `test_simplified_purl_ordering_preserved`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

### Conclusion

The code strips qualifiers via `without_qualifiers()`, and tests explicitly verify that the `?` separator does not appear in response PURLs. The criterion is satisfied.

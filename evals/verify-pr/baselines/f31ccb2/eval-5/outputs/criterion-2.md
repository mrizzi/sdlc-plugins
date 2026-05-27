## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

### Assessment: PASS

**Evidence from the diff:**

Multiple test assertions explicitly verify the absence of `?` in response PURLs:

In `tests/api/purl_recommend.rs` (`test_recommend_purls_basic`):
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The production code in `mod.rs` uses `p.without_qualifiers()` which strips all qualifier key-value pairs, ensuring no `?` appears in the serialized PURL.

**Conclusion:** Both production code and tests confirm qualifier removal. The `contains('?')` assertions provide explicit negative-case coverage.

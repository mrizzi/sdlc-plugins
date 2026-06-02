# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

### Code Evidence

The service layer in `modules/fundamental/src/purl/service/mod.rs` applies `without_qualifiers()` to every PURL before serialization:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (documented in the task as being part of `common/src/purl.rs`) removes all qualifier key-value pairs from the PURL. Since qualifiers in a PURL are encoded as query parameters after a `?` character, calling `without_qualifiers()` ensures no `?` appears in the output string.

### Test Evidence

The PR adds explicit assertions in the updated `test_recommend_purls_basic` test to verify no `?` is present:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly test the criterion's requirement. Additionally, the new `test_simplified_purl_no_version` test in `purl_simplify.rs` includes the same assertion:

```rust
assert!(!body.items[0].purl.contains('?'));
```

And `test_simplified_purl_mixed_types` asserts that even qualifiers with different naming patterns are stripped:

```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

The `test_simplified_purl_ordering_preserved` test also confirms no `?` in paginated results:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### Conclusion

The code uniformly strips qualifiers via `without_qualifiers()`, and multiple tests explicitly assert that `?` does not appear in response PURLs. This criterion is satisfied.

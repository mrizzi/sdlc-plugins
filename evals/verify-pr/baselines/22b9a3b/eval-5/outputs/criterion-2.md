# Criterion 2: Response PURLs do not contain ? query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

## Reasoning

### Implementation

The service layer in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL model before serialization. The `without_qualifiers()` method (documented in the task as part of `common/src/purl.rs`) constructs a PURL representation that excludes all qualifier key-value pairs. Since qualifiers are appended after the `?` separator in the PURL specification, removing qualifiers removes the `?` and everything after it.

### Test Coverage

Multiple tests explicitly assert the absence of `?` in response PURLs:

1. **`test_recommend_purls_basic`** (`tests/api/purl_recommend.rs`):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. **`test_simplified_purl_no_version`** (`tests/api/purl_simplify.rs`):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. **`test_simplified_purl_mixed_types`** (`tests/api/purl_simplify.rs`):
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```
   This checks for a specific qualifier key, confirming qualifier data is absent.

4. **`test_simplified_purl_ordering_preserved`** (`tests/api/purl_simplify.rs`):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

### Structural Guarantee

The absence of qualifiers is guaranteed at the data transformation level (service layer), not at the serialization level. Every PURL passes through `without_qualifiers()` before being wrapped in `PurlSummary`. This means there is no code path that could produce a qualified PURL in the response -- the guarantee is structural, not just tested.

All CI checks pass, confirming these assertions hold at runtime.

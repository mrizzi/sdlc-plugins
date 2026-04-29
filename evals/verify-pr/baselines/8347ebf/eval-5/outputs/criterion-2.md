# Criterion 2: Response PURLs do not contain `?` query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict:** PASS

## Reasoning

### Implementation Evidence

The `without_qualifiers()` method (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) is called on every PURL before it is serialized to string in the service layer. The `PackageUrl` builder constructs PURLs with or without qualifiers, and the `without_qualifiers()` variant produces a PURL string that never includes the `?` separator or any key=value qualifier pairs.

### Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

1. In `test_recommend_purls_basic` (modified):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. In `test_simplified_purl_no_version` (new):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. In `test_simplified_purl_mixed_types` (new):
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```
   This checks for a specific qualifier key rather than the `?` character, but it still validates qualifier absence.

4. In `test_simplified_purl_ordering_preserved` (new):
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

### Conclusion

The implementation strips qualifiers at the service layer before serialization, and four separate tests explicitly assert that response PURLs do not contain `?` or qualifier key-value pairs. This criterion is satisfied.

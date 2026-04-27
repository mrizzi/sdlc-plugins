# Criterion 6 (Test Requirement 1): Update test_recommend_purls_basic

## Criterion Text
Update `test_recommend_purls_basic` to assert versioned PURL without qualifiers.

## Evidence from PR Diff

### Changes in `tests/api/purl_recommend.rs`
The test function `test_recommend_purls_basic` was modified with the following changes:

1. **Doc comment updated** from:
   ```rust
   /// Verifies that basic PURL recommendations return fully qualified PURLs.
   ```
   to:
   ```rust
   /// Verifies that basic PURL recommendations return versioned PURLs without qualifiers.
   ```

2. **Primary assertion changed** from checking a fully qualified PURL with qualifiers:
   ```rust
   assert_eq!(
       body.items[0].purl,
       "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
   );
   ```
   to checking a versioned PURL without qualifiers:
   ```rust
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

3. **New negative assertions added** to explicitly verify no qualifiers are present:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

## Verdict: PASS

The `test_recommend_purls_basic` test was updated to assert the versioned PURL format without qualifiers, including both a positive assertion on the expected format and negative assertions confirming the absence of qualifier separators.

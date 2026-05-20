# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

**What was checked:**
This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

**Evidence from the diff:**

1. **Validation logic (list.rs):** The `validate_license_param` function iterates over each identifier and attempts to parse it as an SPDX expression:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator causes early return on the first invalid identifier. The error is wrapped in `AppError::BadRequest` with a descriptive message that includes the invalid identifier.

2. **Error propagation (list.rs):** In the `list_packages` handler, the validation result is used with the `?` operator:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   If validation fails, the `AppError::BadRequest` propagates as the handler's error response. Per the repository conventions, `AppError` implements `IntoResponse` (defined in `common/src/error.rs`), so `AppError::BadRequest` maps to a 400 HTTP status code.

3. **Error message format:** The error message follows the format `"Invalid SPDX license identifier: INVALID-999"`, providing both a human-readable explanation and the specific offending value.

4. **Test coverage (tests/api/package.rs):** The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
   ```rust
   assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
   ```

**Conclusion:** The implementation validates each license identifier against the SPDX expression parser, returns `AppError::BadRequest` with a descriptive error message for invalid identifiers, and the integration test confirms the 400 status code response. This criterion is satisfied.

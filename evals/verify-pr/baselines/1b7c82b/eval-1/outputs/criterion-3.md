## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Analysis

**What the criterion requires:**
When an invalid SPDX license identifier is provided, the endpoint must return a 400 Bad Request response with an error message explaining the problem.

**Evidence from the PR diff:**

1. **Validation logic (`list.rs`):**
   The `validate_license_param` function iterates over each comma-separated identifier and calls `Expression::parse(id)`. For `INVALID-999`, which is not a valid SPDX expression, `Expression::parse` returns an `Err`. The `map_err` closure converts this into:
   ```rust
   AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   ```
   The `?` operator propagates this error immediately, short-circuiting further processing.

2. **Error propagation (`list.rs`):**
   In the `list_packages` handler, the validation is called as:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   The `?` operator propagates the `AppError::BadRequest` back to the Axum framework, which renders it as a 400 status code with the error message. This is consistent with the repository's error handling pattern documented in `common/src/error.rs` where `AppError` implements `IntoResponse`.

3. **Test coverage (`tests/api/package.rs`):**
   The `test_list_packages_invalid_license_returns_400` test sends `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`. This directly validates the 400 response behavior.

4. **Error message presence:**
   The `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` ensures the response body includes a descriptive error message containing the invalid identifier. The task requires "an error message," which is satisfied by this format string.

**Conclusion:**
The validation correctly rejects invalid SPDX identifiers, returns `AppError::BadRequest` with a descriptive message, and the test confirms the 400 status code. The criterion is satisfied.

## Criterion 3: Invalid License Returns 400

**Text:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict:** PASS

**Reasoning:**

In `validate_license_param`, each license identifier is validated: `Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?;`

When `Expression::parse` fails for an invalid identifier like `INVALID-999`, the error is mapped to `AppError::BadRequest` with a descriptive message, returning 400 Bad Request.

The test `test_list_packages_invalid_license_returns_400` confirms: `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`.

## Review Comment Classification: 30003

**Comment ID:** 30003
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/mod.rs, line 18
**Classification:** nit

### Comment Text

> Nit: `context("SBOM not found")` is misleading here because `.context()` wraps the error message for the anyhow chain -- it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `"Failed to fetch SBOM"` to avoid confusion in error logs.

### Classification Reasoning

The reviewer explicitly labels this as a "Nit" and the feedback is about improving a context string for clarity in error logs. The existing code is functionally correct -- the `.context()` call wraps the error for the anyhow chain, and the actual 404 is properly handled by `ok_or(AppError::NotFound(...))`. The suggested change (`"Failed to fetch SBOM"`) is a minor readability improvement to avoid confusion between the context message and the actual error handling. This does not affect correctness or functionality.

### Action

No sub-task created. Minor style feedback that does not affect correctness.

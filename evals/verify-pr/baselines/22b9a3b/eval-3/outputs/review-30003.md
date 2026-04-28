# Review Comment Classification: 30003

**Comment ID:** 30003
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/mod.rs (line 18)
**Classification:** nit

## Reasoning

The reviewer explicitly labels this feedback as "Nit" at the start of the comment. The comment addresses a misleading error message in the `.context()` call -- the string `"SBOM not found"` is used as an anyhow context wrapper, but the actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. The reviewer suggests changing the context message to `"Failed to fetch SBOM"` to avoid confusion in error logs.

This is a minor clarity improvement in error messaging that does not affect correctness or functionality. The current code works correctly -- the `.context()` wrapping still produces the right error chain, and the 404 response is handled properly. The suggestion only improves log readability.

**Action:** No sub-task created. Minor style feedback that does not affect correctness.

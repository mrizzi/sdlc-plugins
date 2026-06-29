# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

## Verification Result

**Status:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It is documented in the official GitHub REST API documentation.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Evidence

The `PUT` method on the reviews endpoint accepts a `body` parameter and returns the updated review object. This means:

- Submitted reviews **can** be modified after initial submission.
- There is no need to always create a new review; an existing review can be updated in place.

## Suggested Correction

**Original language:**
> PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review

**Corrected language:**
> Update the existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review

The corrected language reflects the actual API capability and avoids unnecessary review proliferation.

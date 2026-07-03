# External API Claim Verification

## Claim Detected

In **Section 4 — Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission — The GitHub API does not support modifying a submitted review."

## Verification

**Source:** GitHub REST API official documentation

The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. The endpoint accepts a `body` parameter (required) and returns the updated review object.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Result: INCORRECT

The claim is **incorrect**. The GitHub REST API supports `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a submitted review. The requirement should be revised to reflect this capability.

## Suggested Correction

**Original:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected:** "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"

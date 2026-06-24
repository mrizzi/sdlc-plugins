# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement context:** The requirement states to "always create a new review" because the GitHub API allegedly does not support modifying a submitted review.

## Verification Finding

**Result: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It accepts a JSON payload with the updated `body` field and returns the updated review object.

**Documentation reference:** GitHub REST API documentation for Pull Request Reviews confirms the `PUT` method is available for updating an existing review.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing PR reviews when re-running evals on the same PR, or create a new review if none exists"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

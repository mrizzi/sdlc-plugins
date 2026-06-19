# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

**Notes from user:** "The GitHub API does not support modifying a submitted review"

## Verification

**Result: INCORRECT**

The GitHub REST API does support updating a submitted pull request review. The following endpoint exists:

- **Method:** `PUT`
- **Endpoint:** `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

This endpoint allows updating the body of a submitted review. The claim that "PR reviews cannot be updated after initial submission" and that "The GitHub API does not support modifying a submitted review" is factually incorrect.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement:** "Update the existing review when re-running evals on the same PR, or create a new review if none exists"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

The corrected language reflects the actual API capability and avoids creating unnecessary duplicate reviews on a PR.

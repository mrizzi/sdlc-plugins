# External API Claim Verification

## Claim Detected

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

## Verification Result

**Status:** INCORRECT

The claim that the GitHub API does not support modifying a submitted review is factually wrong. The GitHub REST API provides the following endpoint for updating a submitted pull request review:

- **Method:** `PUT`
- **Endpoint:** `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review

This endpoint allows updating the body of an existing review after it has been submitted. The `review_id` is obtained from the review creation response or by listing reviews on a pull request.

## Suggested Correction

The requirement should be revised to remove the incorrect claim. Instead of:

> "PR reviews cannot be updated after initial submission so always create a new review"

The corrected language should be:

> "Update the existing review when re-running evals on the same PR, rather than creating duplicate reviews"

This corrected language acknowledges the API capability and leads to a better user experience by avoiding duplicate review comments on the same PR.

## Impact

This correction affects the implementation approach: rather than always creating new reviews (which would clutter the PR with duplicate review entries), the implementation should track the review ID from the initial posting and use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update the review body with the latest eval results.

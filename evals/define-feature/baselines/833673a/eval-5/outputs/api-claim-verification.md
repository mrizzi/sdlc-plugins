# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review"

## Verification

**Method:** WebSearch and WebFetch against official GitHub REST API documentation

**Finding:** The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

**Evidence:**

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation:** [GitHub REST API - Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)
- **Description:** This endpoint allows updating the body of a submitted pull request review. The `review_id` identifies the review to update, and the request body accepts a `body` parameter with the updated review text.

## Result

**Status:** INCORRECT -- the API does support the claimed missing capability.

## Suggested Correction

**Original wording:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected wording:** "Update the existing PR review when re-running evals instead of creating a new review, using `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update an existing review"

The corrected language has been applied in the Feature description preview.

# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claims were identified:

1. **"PR reviews cannot be updated after initial submission so always create a new review"**
2. **"The GitHub API does not support modifying a submitted review"**

These statements assert that the GitHub REST API lacks the capability to update a PR review after it has been submitted.

## Verification Finding

The claim is **incorrect**. The GitHub REST API **does** support updating a submitted pull request review.

**Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`

This endpoint allows modifying the body of a previously submitted review. It accepts the `review_id` of an existing review and a new `body` parameter, enabling updates to the review content after initial submission.

**Documentation reference:** GitHub REST API docs -- "Update a review for a pull request" under the Pull Request Reviews section.

## Suggested Corrected Language

**Original requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

The corrected language reflects that the GitHub REST API supports updating submitted reviews, so the workflow should update an existing review rather than always creating a new one.

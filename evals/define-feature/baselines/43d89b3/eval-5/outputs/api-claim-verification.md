# External API Claim Verification

## Detected Claim

In Section 4 (Requirements), the following requirement contains an incorrect claim about GitHub API capabilities:

> **Requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
> **Notes:** "The GitHub API does not support modifying a submitted review"

The user asserts that (1) PR reviews cannot be updated after initial submission, and (2) the GitHub REST API does not support modifying a submitted review.

## Verification Finding

This claim is **incorrect**. The GitHub REST API **does** support updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It accepts the `review_id` of an existing review and a new `body` parameter, enabling modifications after initial submission.

**Reference:** GitHub REST API documentation - Pull Request Reviews - Update a pull request review.

## Suggested Corrected Language

The requirement and its notes should be updated to reflect that reviews can be updated. Suggested revision:

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review, or `POST` to create a new one | Yes |

This corrected requirement avoids creating duplicate reviews on repeated eval runs by leveraging the GitHub API's update capability.

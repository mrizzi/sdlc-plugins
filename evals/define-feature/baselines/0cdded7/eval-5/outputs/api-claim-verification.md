# External API Claim Verification

## Detected Claim

The Requirements section (row 4) contains the following claims about the GitHub REST API:

1. "PR reviews cannot be updated after initial submission"
2. "The GitHub API does not support modifying a submitted review"

## Verification

These claims are **incorrect**. The GitHub REST API does support updating a submitted pull request review via the following endpoint:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It is documented in the official GitHub REST API reference under Pull Request Reviews.

## Evidence

- **Endpoint**: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Purpose**: Update the body text of a pull request review that has already been submitted
- **Documentation**: [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

## Suggested Corrected Language

**Original requirement**: "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes**: "The GitHub API does not support modifying a submitted review"

**Corrected requirement**: "Update the existing PR review when re-running evals on the same PR, or create a new review if none exists"
**Corrected notes**: "The GitHub REST API supports updating a submitted review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`"

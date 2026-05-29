# External API Claim Verification

## Detected Claim

In Section 4 (Requirements), the following claim was made:

> "PR reviews cannot be updated after initial submission so always create a new review"

With the supporting note:

> "The GitHub API does not support modifying a submitted review"

## Verification Finding

**Status: INCORRECT**

The claim is factually incorrect. The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It is documented in the official GitHub REST API reference under Pull Request Reviews.

## Suggested Corrected Language

**Requirement**: "Update existing PR reviews instead of creating duplicates when re-running evals on the same PR"

**Notes**: "PR reviews can be updated using the GitHub REST API (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`), so update existing reviews instead of always creating new ones"

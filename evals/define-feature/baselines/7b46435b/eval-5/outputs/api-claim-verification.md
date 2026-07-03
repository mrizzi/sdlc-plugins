# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API does not support modifying a PR review after it has been submitted, matching the detection pattern "X cannot be updated after creation" / "The API does not support Y".

## Verification

**Result: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts an updated `body` parameter and modifies the review in place. It is documented in the official GitHub REST API reference under the Pull Request Reviews section.

**Evidence:**
- Endpoint: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- Method: `PUT`
- Purpose: Update the body text of a pull request review that has already been submitted
- Documentation: GitHub REST API > Pull Requests > Reviews > Update a pull request review

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one"

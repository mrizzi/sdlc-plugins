# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Claim type:** Assertion that an external API lacks a capability

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint to update a submitted review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted pull request review. It accepts a JSON payload with the updated `body` field and returns the updated review object.

**Documentation reference:** GitHub REST API documentation — Pull Request Reviews — Update a pull request review

### Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected requirement:**
> Update the existing PR review when re-running evals, or create a new review if none exists

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review

The correction changes the design approach from always creating new reviews (based on a false limitation) to updating existing reviews when possible, which avoids cluttering the PR with duplicate review comments.

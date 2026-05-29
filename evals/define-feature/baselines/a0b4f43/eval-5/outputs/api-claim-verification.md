# External API Claim Verification

## Detected Claim

In **Section 4 — Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This is a claim asserting a limitation of an external API (GitHub REST API) — specifically, that submitted PR reviews cannot be modified.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted pull request review. It accepts a JSON payload with a `body` field containing the updated review text.

**Documentation reference:** GitHub REST API — Pull Request Reviews — "Update a review for a pull request"

### Conclusion

The assertion that "The GitHub API does not support modifying a submitted review" is factually incorrect. The `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint exists and can be used to update the body of a previously submitted review.

## Suggested Corrected Language

**Original requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Corrected requirement:**
> Update the existing PR review when re-running evals on the same PR, rather than creating a new review each time

**Original notes:**
> The GitHub API does not support modifying a submitted review

**Corrected notes:**
> Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review

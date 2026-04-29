# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review" with note "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

**Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review

This endpoint allows you to update the body of a submitted review. The request accepts a `body` parameter (string, required) containing the updated text of the review.

### Suggested Correction

The requirement should be revised to remove the incorrect claim about API limitations. Instead of:

> "PR reviews cannot be updated after initial submission so always create a new review" / "The GitHub API does not support modifying a submitted review"

The corrected language should be:

> "Update existing eval review if one was previously posted; create a new review only on first run" / "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

This correction allows the Feature to leverage the update capability, avoiding duplicate review comments on PRs and providing a cleaner reviewer experience.

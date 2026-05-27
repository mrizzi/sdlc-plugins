# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update an existing pull request review.

## Verification Finding

**Result: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's top-level comment body. It is documented in the GitHub REST API reference under Pull Request Reviews.

**Reference:** [GitHub REST API -- Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Suggested Corrected Language

**Original requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews can be updated via the GitHub API, but create a new review when eval results have changed significantly | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` for minor updates; create a new review for substantial changes to preserve the review timeline | Yes |

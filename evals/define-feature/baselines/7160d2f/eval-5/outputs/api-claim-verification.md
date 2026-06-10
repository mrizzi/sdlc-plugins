# External API Claim Verification

## Detected Claim

The following claim was found in Section 4 (Requirements):

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

## Verification Finding

**Status**: INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It accepts the `review_id` of an existing review and a new `body` parameter to update the review content.

## Reference

GitHub REST API documentation: [Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

Endpoint: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`

## Suggested Corrected Language

**Original requirement**: "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement**: "Update the existing eval review on subsequent runs instead of creating duplicate reviews, using the GitHub REST API's update review endpoint (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`)"

**Original notes**: "The GitHub API does not support modifying a submitted review"

**Corrected notes**: "Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review; store the review ID to enable updates on re-runs"

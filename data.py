query = """
{
  user(login: "nameholder") {
    contributionsCollection(from: "startholder", to: "endholder") {
      issueContributions(first: 100) {
        totalCount
        nodes {
          issue {
            repository {
              nameWithOwner
            }
            url
            title
          }
        }
      }
      pullRequestContributions(first: 100) {
        totalCount
        nodes {
          pullRequest {
            title
            url
            repository {
              nameWithOwner
            }
          }
        }
      }
      pullRequestReviewContributions(first: 100) {
        totalCount
        nodes {
          pullRequest {
            title
            url
            repository {
              nameWithOwner
            }
          }
          pullRequestReview {
            url
          }
        }
      }
    }
    issueComments(last: 100) {
      nodes {
        issue {
          title
          createdAt
          url
          id
          repository {
            nameWithOwner
          }
        }
      }
    }
  }
}
"""

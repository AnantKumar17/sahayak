import { ReviewResponse, PastReview } from '../types';

interface Props {
  review: ReviewResponse | null;
  pastReviews: PastReview[];
  prComments: Array<{ pr_number: number; text: string; similarity: number }> | null;
}

function ReviewDisplay({ review, pastReviews, prComments }: Props) {
  return (
    <div>
      <h2>Code Review</h2>
      {review ? (
        <div>
          <p><strong>Readability:</strong> {review.readability}</p>
          <p><strong>Security:</strong> {review.security}</p>
          <p><strong>Performance:</strong> {review.performance}</p>
          <p><strong>Best Practices:</strong> {review.best_practices}</p>
          <p><strong>Bugs:</strong> {review.bugs}</p>
          <p><strong>Overall Analysis:</strong> {review.overall_analysis}</p>
          <p><strong>Suggested Refactored Code:</strong></p>
          <pre>{review.suggested_refactored_code}</pre>
        </div>
      ) : (
        <p>No review available.</p>
      )}

      <h2>Past Reviews</h2>
      {pastReviews.length > 0 ? (
        <ul>
          {pastReviews.map((review, index) => (
            <li key={index}>
              <p>{review.text}</p>
              <p>Similarity: {(review.similarity * 100).toFixed(2)}%</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No past reviews found.</p>
      )}

      <h2>Matching PR Comments</h2>
      {prComments && prComments.length > 0 ? (
        <ul>
          {prComments.map((comment, index) => (
            <li key={index}>
              <p><strong>PR #{comment.pr_number}:</strong> {comment.text}</p>
              <p>Similarity: {(comment.similarity * 100).toFixed(2)}%</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No matching PR comments found.</p>
      )}
    </div>
  );
}

export default ReviewDisplay;
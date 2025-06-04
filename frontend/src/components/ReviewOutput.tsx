// src/components/ReviewOutput.tsx
import { ReviewResponse } from '../types';

interface Props {
  review: ReviewResponse;
}

function ReviewOutput({ review }: Props) {
  return (
    <div className="review-output">
      <h3>Code Review</h3>
      <p><strong>Readability:</strong> {review.readability}</p>
      <p><strong>Security:</strong> {review.security}</p>
      <p><strong>Performance:</strong> {review.performance}</p>
      <p><strong>Best Practices:</strong> {review['best_practices']}</p>
      <p><strong>Bugs:</strong> {review.bugs}</p>
      <p><strong>Overall Analysis:</strong> {review['overall_analysis']}</p>
    </div>
  );
}

export default ReviewOutput;
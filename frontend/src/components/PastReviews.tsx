import { PastReview } from '../types';

interface Props {
  reviews: PastReview[];
}

function PastReviews({ reviews }: Props) {
  return (
    <div className="past-reviews">
      <h3>Past Reviews</h3>
      {reviews.length === 0 ? (
        <p>No past reviews available.</p>
      ) : (
        reviews.map((review, index) => (
          <div key={index} className="past-review">
            <p><strong>Review {index + 1} (Similarity: {(review.similarity * 100).toFixed(2)}%):</strong></p>
            <p>{review.text}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default PastReviews;
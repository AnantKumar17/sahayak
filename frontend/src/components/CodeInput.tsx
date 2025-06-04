// import { useState } from 'react';
// import axios from 'axios';
// import { ReviewResponse, PastReview } from '../types';

// interface Props {
//   code: string;
//   setCode: (code: string) => void;
//   prNumber: number | undefined;
//   setPrNumber: (prNumber: number | undefined) => void;
//   setReview: (review: ReviewResponse | null) => void;
//   setPastReviews: (reviews: PastReview[]) => void;
//   setPrComment: (comment: string | null) => void;
// }

// function CodeInput({ code, setCode, prNumber, setPrNumber, setReview, setPastReviews, setPrComment }: Props) {
//   const [error, setError] = useState('');

//   const handleSubmit = async () => {
//     if (!code.trim()) {
//       setError('Please enter a code snippet.');
//       return;
//     }
//     setError('');

//     try {
//       const payload: { code: string; pr_number?: number } = { code };
//       if (prNumber !== undefined) {
//         payload.pr_number = prNumber; // Fixed typo
//       }

//       const reviewPromise = axios.post('http://127.0.0.1:8000/review', payload)
//         .catch((err) => {
//           console.error('Review error:', err);
//           return { data: null };
//         });

//       const pastReviewsPromise = axios.get('http://127.0.0.1:8000/past_reviews', { params: { code } })
//         .catch((err) => {
//           console.error('Past reviews error:', err);
//           return { data: { past_reviews: [] } };
//         });

//       const prCommentPromise = prNumber !== undefined
//         ? axios.get(`http://127.0.0.1:8000/pr_comment/${prNumber}`)
//           .catch((err) => {
//             console.error('PR comment error:', err);
//             return { data: { comments: [] } };
//           })
//         : Promise.resolve({ data: { comments: [] } });

//       const [reviewRes, pastReviewsRes, prCommentRes] = await Promise.all([
//         reviewPromise,
//         pastReviewsPromise,
//         prCommentPromise,
//       ]);

//       if (reviewRes.data) {
//         setReview(reviewRes.data);
//       } else {
//         setError('Failed to fetch review.');
//       }

//       setPastReviews(pastReviewsRes.data.past_reviews.slice(0, 2));
//       setPrComment(prCommentRes.data.comments[0] || null);
//     } catch (error) {
//       console.error('Error in handleSubmit:', error);
//       setError('Error fetching review response. Please try again.');
//     }
//   };

//   return (
//     <div>
//       <textarea
//         value={code}
//         onChange={(e) => setCode(e.target.value)}
//         placeholder="Enter your code snippet..."
//         rows={10}
//       />
//       <input
//         type="number"
//         value={prNumber || ''}
//         onChange={(e) => setPrNumber(e.target.value ? parseInt(e.target.value) : undefined)}
//         placeholder="Enter PR number (optional)"
//       />
//       <button onClick={handleSubmit}>Review Code</button>
//       {error && <p style={{ color: 'red' }}>{error}</p>}
//     </div>
//   );
// }

// export default CodeInput;

import { useState } from 'react';
import axios from 'axios';
import { ReviewResponse, PastReview } from '../types';

interface Props {
  code: string;
  setCode: (code: string) => void;
  setReview: (review: ReviewResponse | null) => void;
  setPastReviews: (reviews: PastReview[]) => void;
  setPrComments: (comments: Array<{ pr_number: number; text: string; similarity: number }> | null) => void;
}

function CodeInput({ code, setCode, setReview, setPastReviews, setPrComments }: Props) {
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!code.trim()) {
      setError('Please enter a code snippet.');
      return;
    }
    setError('');

    try {
      const payload = { code };

      const reviewPromise = axios.post('http://127.0.0.1:8000/review', payload)
        .catch((err) => {
          console.error('Review error:', err);
          return { data: null };
        });

      const pastReviewsPromise = axios.get('http://127.0.0.1:8000/past_reviews', { params: { code } })
        .catch((err) => {
          console.error('Past reviews error:', err);
          return { data: { past_reviews: [] } };
        });

      const [reviewRes, pastReviewsRes] = await Promise.all([
        reviewPromise,
        pastReviewsPromise,
      ]);

      if (reviewRes.data) {
        setReview(reviewRes.data);
        setPrComments(reviewRes.data.pr_comments || null);
      } else {
        setError('Failed to fetch review.');
      }

      setPastReviews(pastReviewsRes.data.past_reviews.slice(0, 2));
    } catch (error) {
      console.error('Error in handleSubmit:', error);
      setError('Error fetching review response. Please try again.');
    }
  };

  return (
    <div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="Enter your code snippet..."
        rows={10}
      />
      <button onClick={handleSubmit}>Review Code</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default CodeInput;
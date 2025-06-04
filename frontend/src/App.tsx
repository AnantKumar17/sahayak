// // frontend/src/App.tsx
// import { useState } from 'react';
// import './App.css';
// import CodeInput from './components/CodeInput';
// import ReviewOutput from './components/ReviewOutput';
// import RefactoredCode from './components/RefactoredCode';
// import PastReviews from './components/PastReviews';
// import BarChart from './components/BarChart';
// import FollowUp from './components/FollowUp';
// import { ReviewResponse, PastReview } from './types';

// function App() {
//   const [code, setCode] = useState('');
//   const [prNumber, setPrNumber] = useState<number | undefined>(undefined);
//   const [review, setReview] = useState<ReviewResponse | null>(null);
//   const [pastReviews, setPastReviews] = useState<PastReview[]>([]);
//   const [prComment, setPrComment] = useState<string | null>(null);
//   const [showRefactored, setShowRefactored] = useState(false);

//   return (
//     <div className="app-container">
//       <header className="header">
//         <h1>Sahayak Code Review Dashboard</h1>
//       </header>
//       <main>
//         <CodeInput
//           code={code}
//           setCode={setCode}
//           prNumber={prNumber}
//           setPrNumber={setPrNumber}
//           setReview={setReview}
//           setPastReviews={setPastReviews}
//           setPrComment={setPrComment}
//         />
//         {review && (
//           <div className="main-content">
//             <div className="review-section">
//               <ReviewOutput review={review} />
//               <button
//                 className="toggle-button"
//                 onClick={() => setShowRefactored(!showRefactored)}
//               >
//                 {showRefactored ? 'Hide Refactored Code' : 'Show Refactored Code'}
//               </button>
//               {showRefactored && <RefactoredCode code={review['suggested_refactored_code']} />}
//             </div>
//             <div className="past-reviews-section">
//               {pastReviews.length > 0 && (
//                 <>
//                   <PastReviews reviews={pastReviews} />
//                   <BarChart reviews={pastReviews} />
//                 </>
//               )}
//             </div>
//           </div>
//         )}
//         {review && (
//           <div className="bottom-section">
//             <div className="followup-section">
//               <FollowUp review={JSON.stringify(review)} />
//             </div>
//             <div className="pr-comment-section">
//               {prComment ? (
//                 <div className="pr-comment">
//                   <h3>PR #{prNumber} Comment</h3>
//                   <p>{prComment}</p>
//                 </div>
//               ) : (
//                 <div className="pr-comment">
//                   <h3>PR Comment</h3>
//                   <p>No PR comment found, as PR number not provided or invalid.</p>
//                 </div>
//               )}
//             </div>
//           </div>
//         )}
//       </main>
//     </div>
//   );
// }

// export default App;


import { useState } from 'react';
import './App.css';
import CodeInput from './components/CodeInput';
import ReviewDisplay from './components/ReviewDisplay';
import RefactoredCode from './components/RefactoredCode';
import BarChart from './components/BarChart';
import FollowUp from './components/FollowUp';
import { ReviewResponse, PastReview } from './types';

function App() {
  const [code, setCode] = useState('');
  const [review, setReview] = useState<ReviewResponse | null>(null);
  const [pastReviews, setPastReviews] = useState<PastReview[]>([]);
  const [prComments, setPrComments] = useState<Array<{ pr_number: number; text: string; similarity: number }> | null>(null);
  const [showRefactored, setShowRefactored] = useState(false);

  return (
    <div className="app-container">
      <header className="header">
        <h1>Sahayak Code Review Dashboard</h1>
      </header>
      <main>
        <CodeInput
          code={code}
          setCode={setCode}
          setReview={setReview}
          setPastReviews={setPastReviews}
          setPrComments={setPrComments}
        />
        {review && (
          <div className="main-content">
            <div className="review-section">
              <ReviewDisplay review={review} pastReviews={pastReviews} prComments={prComments} />
              <button
                className="toggle-button"
                onClick={() => setShowRefactored(!showRefactored)}
              >
                {showRefactored ? 'Hide Refactored Code' : 'Show Refactored Code'}
              </button>
              {showRefactored && <RefactoredCode code={review['suggested_refactored_code']} />}
            </div>
            {pastReviews.length > 0 && (
              <div className="past-reviews-section">
                <BarChart reviews={pastReviews} />
              </div>
            )}
          </div>
        )}
        {review && (
          <div className="bottom-section">
            <div className="followup-section">
              <FollowUp review={JSON.stringify(review)} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
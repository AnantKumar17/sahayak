// src/components/FollowUp.tsx
import { useState } from 'react';
import axios from 'axios';
import { FollowUpResponse } from '../types';

function FollowUp({ review }: { review: string }) {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState<FollowUpResponse | null>(null);
  const [error, setError] = useState('');

  const handleFollowUp = async () => {
    if (!question.trim()) {
      setError('Please enter a follow-up question.');
      return;
    }
    setError('');

    try {
      const res = await axios.post('http://127.0.0.1:8000/followup', { review, question });
      setResponse(res.data);
    } catch (error) {
      setError('Error fetching follow-up response.');
    }
  };

  return (
    <div>
      <h3>Follow-up Question</h3>
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Enter your follow-up question..."
      />
      <button onClick={handleFollowUp}>Submit</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {response && (
        <div>
          <p><strong>Response:</strong> {response.response}</p>
          {response['suggested refactored code'] && (
            <pre><strong>Refactored Code:</strong><br/>{response['suggested refactored code']}</pre>
          )}
        </div>
      )}
    </div>
  );
}

export default FollowUp;
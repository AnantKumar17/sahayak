// // src/types.ts
// export interface ReviewResponse {
//   readability: string;
//   security: string;
//   performance: string;
//   'best practices': string;
//   bugs: string;
//   'overall analysis': string;
//   'suggested refactored code': string;
// }

// export interface PastReview {
//   text: string;
//   similarity: number;
// }

// export interface FollowUpResponse {
//   response: string;
//   'suggested refactored code'?: string;
// }

export interface ReviewResponse {
  readability: string;
  security: string;
  performance: string;
  best_practices: string;
  bugs: string;
  overall_analysis: string;
  'suggested_refactored_code': string;
  pr_comments?: Array<{ pr_number: number; text: string; similarity: number }>;
}

export interface PastReview {
  text: string;
  similarity: number;
}

export interface FollowUpResponse {
  response: string;
  'suggested refactored code'?: string;
}

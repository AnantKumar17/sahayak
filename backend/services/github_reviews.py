# # backend/services/github_reviews.py
# import requests
# import os
# import logging
# from fastapi import HTTPException
# from typing import List, Optional

# from dotenv import load_dotenv
# load_dotenv()  # Add at the top of github_reviews.py

# # Logging Configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)

# # class GitHubReviewService:
# #     def __init__(self):
# #         self.github_token = os.getenv("GITHUB_TOKEN")
# #         self.github_repo = os.getenv("GITHUB_REPO", "AnantKumar17/sahayak")
# #         self.base_url = f"https://api.github.com/repos/{self.github_repo}"
        
# #         if not self.github_token:
# #             logger.error("GITHUB_TOKEN environment variable not set")
# #             raise ValueError("GITHUB_TOKEN environment variable is required")

# #     def fetch_past_reviews(self, pr_number: int) -> List[str]:
# #         """
# #         Fetch past PR issue comments from GitHub API.
# #         """
# #         try:
# #             url = f"{self.base_url}/issues/{pr_number}/comments"  # Changed to issues/comments endpoint
# #             headers = {
# #                 "Authorization": f"token {self.github_token}",
# #                 "Accept": "application/vnd.github.v3+json"
# #             }
            
# #             response = requests.get(url, headers=headers, timeout=10)
            
# #             if response.status_code == 200:
# #                 comments = response.json()
# #                 comment_bodies = [comment["body"] for comment in comments if comment.get("body")]
# #                 logger.info(f"Fetched {len(comment_bodies)} comments for PR #{pr_number}")
# #                 return comment_bodies
# #             elif response.status_code == 404:
# #                 logger.warning(f"Pull request #{pr_number} not found")
# #                 raise HTTPException(status_code=404, detail=f"Pull request #{pr_number} not found")
# #             elif response.status_code == 403:
# #                 logger.error("GitHub API authentication failed")
# #                 raise HTTPException(status_code=403, detail="Invalid or insufficient GitHub token permissions")
# #             elif response.status_code == 429:
# #                 logger.error("GitHub API rate limit exceeded")
# #                 raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded")
# #             else:
# #                 logger.error(f"GitHub API error: {response.status_code} - {response.text}")
# #                 raise HTTPException(status_code=response.status_code, detail="Failed to fetch GitHub comments")
                
# #         except requests.RequestException as e:
# #             logger.error(f"Network error while fetching GitHub comments: {str(e)}")
# #             raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")

# #     def fetch_pr_comments_for_context(self, pr_number: int) -> str:
# #         """
# #         Fetch and format past PR issue comments for use as context in AI prompts.
# #         """
# #         comments = self.fetch_past_reviews(pr_number)
# #         if not comments:
# #             return "No relevant GitHub pull request comments found."
        
# #         formatted_comments = "\n".join([f"PR Comment: {comment}" for comment in comments])
# #         return f"GitHub PR #{pr_number} Comments:\n{formatted_comments}"

# # github_service = GitHubReviewService()

# class GitHubReviewService:
#     def __init__(self):
#         self.github_token = os.getenv("GITHUB_TOKEN")
#         self.github_repo = os.getenv("GITHUB_REPO", "AnantKumar17/sahayak")
#         self.base_url = f"https://api.github.com/repos/{self.github_repo}"
        
#         if not self.github_token:
#             logger.error("GITHUB_TOKEN environment variable not set")
#             raise ValueError("GITHUB_TOKEN environment variable is required")

#     def fetch_past_reviews(self, pr_number: int) -> List[str]:
#         """
#         Fetch past PR issue comments from GitHub API.
#         """
#         try:
#             url = f"{self.base_url}/issues/{pr_number}/comments"
#             headers = {
#                 "Authorization": f"token {self.github_token}",
#                 "Accept": "application/vnd.github.v3+json"
#             }
            
#             response = requests.get(url, headers=headers, timeout=10)
            
#             if response.status_code == 200:
#                 comments = response.json()
#                 comment_bodies = [comment["body"] for comment in comments if comment.get("body")]
#                 logger.info(f"Fetched {len(comment_bodies)} comments for PR #{pr_number}")
#                 for i, comment in enumerate(comment_bodies, 1):
#                     logger.info(f"PR #{pr_number} Comment {i}: {comment}")
#                 return comment_bodies
#             elif response.status_code == 404:
#                 logger.warning(f"Pull request #{pr_number} not found")
#                 raise HTTPException(status_code=404, detail=f"Pull request #{pr_number} not found")
#             elif response.status_code == 403:
#                 logger.error("GitHub API authentication failed")
#                 raise HTTPException(status_code=403, detail="Invalid or insufficient GitHub token permissions")
#             elif response.status_code == 429:
#                 logger.error("GitHub API rate limit exceeded")
#                 raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded")
#             else:
#                 logger.error(f"GitHub API error: {response.status_code} - {response.text}")
#                 raise HTTPException(status_code=response.status_code, detail="Failed to fetch GitHub comments")
                
#         except requests.RequestException as e:
#             logger.error(f"Network error while fetching GitHub comments: {str(e)}")
#             raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")

#     def fetch_pr_comments_for_context(self, pr_number: int) -> str:
#         """
#         Fetch and format past PR issue comments for use as context in AI prompts.
#         """
#         comments = self.fetch_past_reviews(pr_number)
#         if not comments:
#             return "No relevant GitHub pull request comments found."
        
#         formatted_comments = "\n".join([f"PR Comment: {comment}" for comment in comments])
#         return f"GitHub PR #{pr_number} Comments:\n{formatted_comments}"

# github_service = GitHubReviewService()

import os
import logging
from github import Github
from fastapi import HTTPException
from typing import List, Dict
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from services.rag_storage import save_pr_comments_to_faiss

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize GitHub client
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "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")
g = Github(GITHUB_TOKEN)

# Initialize embedding model
model = SentenceTransformer('BAAI/bge-m3')

class GitHubService:
    def fetch_pr_comments(self, repo_name: str, pr_number: int) -> List[str]:
        """
        Fetches all comments for a specific PR in a repository.
        """
        try:
            repo = g.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            comments = pr.get_issue_comments()
            comment_texts = [comment.body for comment in comments]
            logger.info(f"Fetched {len(comment_texts)} comments for PR #{pr_number}")
            return comment_texts
        except Exception as e:
            logger.error(f"Failed to fetch PR comments: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch PR comments: {str(e)}")

    def fetch_pr_comments_for_context(self, pr_number: int) -> str:
        """
        Fetches and formats PR comments for context in AI review (for legacy use).
        """
        try:
            repo_name = os.getenv("REPO_NAME", "owner/repo")  # Replace with actual repo
            comments = self.fetch_pr_comments(repo_name, pr_number)
            formatted_comments = "\n".join([f"Comment {i+1}: {comment}" for i, comment in enumerate(comments)])
            return formatted_comments if comments else "No comments found."
        except Exception as e:
            logger.error(f"Error formatting PR comments: {str(e)}")
            return "Unable to fetch GitHub pull request reviews."

    def cache_all_pr_comments(self, repo_name: str) -> None:
        """
        Fetches all PR comments from a repository and saves them to FAISS index.
        """
        try:
            repo = g.get_repo(repo_name)
            prs = repo.get_pulls(state='all')
            comments_data = []
            for pr in prs:
                comments = pr.get_issue_comments()
                for comment in comments:
                    comments_data.append({
                        "pr_number": pr.number,
                        "text": comment.body,
                        "embedding": model.encode(comment.body, convert_to_numpy=True)
                    })
            save_pr_comments_to_faiss(comments_data)
            logger.info(f"Cached {len(comments_data)} PR comments for {repo_name}")
        except Exception as e:
            logger.error(f"Failed to cache PR comments: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to cache PR comments: {str(e)}")

github_service = GitHubService()
# backend/services/github_reviews.py
import requests
import os
import logging
from fastapi import HTTPException
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()  # Add at the top of github_reviews.py

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

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
#             url = f"{self.base_url}/issues/{pr_number}/comments"  # Changed to issues/comments endpoint
#             headers = {
#                 "Authorization": f"token {self.github_token}",
#                 "Accept": "application/vnd.github.v3+json"
#             }
            
#             response = requests.get(url, headers=headers, timeout=10)
            
#             if response.status_code == 200:
#                 comments = response.json()
#                 comment_bodies = [comment["body"] for comment in comments if comment.get("body")]
#                 logger.info(f"Fetched {len(comment_bodies)} comments for PR #{pr_number}")
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

class GitHubReviewService:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "AnantKumar17/sahayak")
        self.base_url = f"https://api.github.com/repos/{self.github_repo}"
        
        if not self.github_token:
            logger.error("GITHUB_TOKEN environment variable not set")
            raise ValueError("GITHUB_TOKEN environment variable is required")

    def fetch_past_reviews(self, pr_number: int) -> List[str]:
        """
        Fetch past PR issue comments from GitHub API.
        """
        try:
            url = f"{self.base_url}/issues/{pr_number}/comments"
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                comments = response.json()
                comment_bodies = [comment["body"] for comment in comments if comment.get("body")]
                logger.info(f"Fetched {len(comment_bodies)} comments for PR #{pr_number}")
                for i, comment in enumerate(comment_bodies, 1):
                    logger.info(f"PR #{pr_number} Comment {i}: {comment}")
                return comment_bodies
            elif response.status_code == 404:
                logger.warning(f"Pull request #{pr_number} not found")
                raise HTTPException(status_code=404, detail=f"Pull request #{pr_number} not found")
            elif response.status_code == 403:
                logger.error("GitHub API authentication failed")
                raise HTTPException(status_code=403, detail="Invalid or insufficient GitHub token permissions")
            elif response.status_code == 429:
                logger.error("GitHub API rate limit exceeded")
                raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded")
            else:
                logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch GitHub comments")
                
        except requests.RequestException as e:
            logger.error(f"Network error while fetching GitHub comments: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")

    def fetch_pr_comments_for_context(self, pr_number: int) -> str:
        """
        Fetch and format past PR issue comments for use as context in AI prompts.
        """
        comments = self.fetch_past_reviews(pr_number)
        if not comments:
            return "No relevant GitHub pull request comments found."
        
        formatted_comments = "\n".join([f"PR Comment: {comment}" for comment in comments])
        return f"GitHub PR #{pr_number} Comments:\n{formatted_comments}"

github_service = GitHubReviewService()
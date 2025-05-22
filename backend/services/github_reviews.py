import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "AnantKumar/sahayak"  # Replace with actual repo

def fetch_past_reviews(pr_number):
    """Fetch past PR reviews from GitHub API."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls/{pr_number}/reviews"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        reviews = response.json()
        return [review['body'] for review in reviews if 'body' in review]
    return []

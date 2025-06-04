import os
from services.github_reviews import github_service
from services.rag_storage import save_pr_comments_to_faiss
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

model = SentenceTransformer('BAAI/bge-m3')

def update_pr_comments_cache():
    """
    Updates the FAISS index with PR comments from the repository.
    """
    try:
        repo_name = os.getenv("REPO_NAME", "AnantKumar17/sahayak")  # Replace with actual repo
        github_service.cache_all_pr_comments(repo_name)
        logger.info("PR comments cache updated successfully")
    except Exception as e:
        logger.error(f"Failed to update PR comments cache: {str(e)}")

if __name__ == "__main__":
    update_pr_comments_cache()
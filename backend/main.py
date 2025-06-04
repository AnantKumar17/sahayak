# from fastapi import FastAPI, BackgroundTasks
# import uvicorn
# import json
# import asyncio
# import logging
# from typing import Optional
# from services.github_reviews import github_service
# from services.gpt_api import query_gpt
# from services.gpt_api import followup_query
# from services.rag_storage import retrieve_similar_reviews
# #from services.starcoder_api import query_star_coder_for_comment
# # from services.rag_storage import retrieve_similar_reviews
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Change * to specific frontend URL if needed
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# class CodeSnippet(BaseModel):
#     code: str
#     pr_number: Optional[int] = None  # New field for PR number

# class FollowUpRequest(BaseModel):
    
#     review: str     # Original AI review
#     question: str   # User's follow-up question



# @app.post("/review")
# def review_code(snippet: CodeSnippet):
#     logger.info(f"Reviewing code with PR number: {snippet.pr_number}")
#     return query_gpt(snippet.code, snippet.pr_number)

# # @app.get("/past_reviews")
# # def get_past_reviews(code: str):
# #     """Retrieve past reviews for a given code snippet."""
# #     return {"past_reviews": retrieve_similar_reviews(code)}

# @app.get("/past_reviews")
# def get_past_reviews(snippet: CodeSnippet):
#     """Retrieve past reviews for a given code snippet."""
#     reviews = retrieve_similar_reviews(snippet.code)
#     return {"past_reviews": reviews}

# @app.get("/test")
# def test_func():
#     return "Application is running"

# @app.post("/followup")
# def followup_review(request: FollowUpRequest):
#     return followup_query(request.review, request.question)

# @app.get("/pr_comment/{pr_number}")
# def get_pr_comment(pr_number: int):
#     """Fetch GitHub PR comments for a given PR number."""
#     comments = github_service.fetch_past_reviews(pr_number)
#     return {"comments": comments}


# if __name__ == "__main__":
#     import logging

#     # Configure logging
#     logging.basicConfig(level=logging.DEBUG)

#     # Run Uvicorn with detailed logs
#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")



from fastapi import FastAPI, BackgroundTasks
import uvicorn
import json
import asyncio
from services.gpt_api import query_gpt, followup_query
from services.rag_storage import retrieve_similar_reviews
from services.github_reviews import github_service
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeSnippet(BaseModel):
    code: str
    pr_number: int | None = None

class FollowUpRequest(BaseModel):
    review: str
    question: str

@app.post("/review")
def review_code(snippet: CodeSnippet):
    logger.info(f"Reviewing code with PR number: {snippet.pr_number}")
    return query_gpt(snippet.code, snippet.pr_number)

@app.get("/past_reviews")
def get_past_reviews(code: str):
    """Retrieve past reviews for a given code snippet."""
    return {"past_reviews": retrieve_similar_reviews(code)}

@app.post("/followup")
def followup_review(request: FollowUpRequest):
    return followup_query(request.review, request.question)

@app.get("/pr_comment/{pr_number}")
def get_pr_comment(pr_number: int):
    """Fetch comments for a given PR number."""
    comments = github_service.fetch_past_reviews(pr_number)
    return {"comments": comments}

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
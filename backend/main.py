from fastapi import FastAPI, BackgroundTasks
import uvicorn
import json
import asyncio
import logging
from typing import Optional
from services.github_reviews import github_service
from services.gpt_api import query_gpt
from services.gpt_api import followup_query
from services.rag_storage import retrieve_similar_reviews
#from services.starcoder_api import query_star_coder_for_comment
# from services.rag_storage import retrieve_similar_reviews
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change * to specific frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# class CodeSnippet(BaseModel):
#     code: str

class CodeSnippet(BaseModel):
    code: str
    pr_number: Optional[int] = None  # New field for PR number

class FollowUpRequest(BaseModel):
    
    review: str     # Original AI review
    question: str   # User's follow-up question

# @app.get("/")
# async def root():
#     return {"message": "API is running"}

# @app.post("/review")
# def review_code(snippet: CodeSnippet):
#     print("Reviewing code function")
#     #review = query_star_coder(snippet.code)
#     #print(json.dumps(review, indent=4))
#     #background_tasks.add_task(query_star_coder)
#     return query_gpt(snippet.code)

@app.post("/review")
def review_code(snippet: CodeSnippet):
    logger.info(f"Reviewing code with PR number: {snippet.pr_number}")
    return query_gpt(snippet.code, snippet.pr_number)

@app.get("/past_reviews")
def get_past_reviews(snippet: CodeSnippet):
    """Retrieve past reviews for a given code snippet."""
    return {"past_reviews": retrieve_similar_reviews(snippet.code)}

@app.get("/test")
def test_func():
    return "Application is running"

@app.post("/followup")
def followup_review(request: FollowUpRequest):
    return followup_query(request.review, request.question)


# @app.get("/past_reviews")
# def get_past_reviews(code: str):
#     """Retrieve past reviews for a given code snippet."""
#     return {"past_reviews": retrieve_similar_reviews(code)}

# @app.post("/inline_comment")
# def generate_inline_comment(snippet: CodeSnippet):
#     return query_star_coder_for_comment(snippet.code)


if __name__ == "__main__":
    import logging

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Run Uvicorn with detailed logs
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

# if __name__ == "__main__":
#     try:
#         uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
#     except KeyboardInterrupt:
#         print("\n[INFO] Server stopped manually.")



# from fastapi import FastAPI, BackgroundTasks, Depends
# import uvicorn
# import json
# import sqlite3
# from services.deepseek_api import query_deepseek
# from services.rag_storage import retrieve_similar_reviews
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change * to specific frontend URL if needed
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

# class CodeSnippet(BaseModel):
#     code: str

# # Database connection dependency
# def get_db():
#     db = sqlite3.connect("reviews.db", check_same_thread=False)
#     db.row_factory = sqlite3.Row  # Allows fetching results as dict-like objects
#     try:
#         yield db  # Provides the database connection
#     finally:
#         db.close()  # Ensures the connection is closed after the request

# @app.post("/review")
# def review_code(snippet: CodeSnippet, db: sqlite3.Connection = Depends(get_db)):
#     """Review code using DeepSeek API"""
#     print("Reviewing code function")
#     return query_deepseek(snippet.code)

# @app.get("/past_reviews")
# def get_past_reviews(snippet: CodeSnippet, db: sqlite3.Connection = Depends(get_db)):
#     """Retrieve past reviews for a given code snippet."""
#     return {"past_reviews": retrieve_similar_reviews(snippet.code, db)}

# @app.get("/test")
# def test_func():
#     return "Application is running"

# if __name__ == "__main__":
#     import logging

#     logging.basicConfig(level=logging.DEBUG)

#     uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")


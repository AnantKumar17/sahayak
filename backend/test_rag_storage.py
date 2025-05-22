# test_rag_storage.py

#from rag_storage import store_review, retrieve_similar_reviews, reset_storage
import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from services.rag_storage import AdvancedCodeReviewRAG

rag_system = AdvancedCodeReviewRAG()
# # Load embedding model (you can replace with a better one if needed)
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# # Initialize FAISS index for fast retrieval
# embedding_dim = 384  # Adjust if using a different embedding model
# faiss_index = faiss.IndexFlatL2(embedding_dim)
# stored_embeddings = []  # To track added embeddings (not persistent)

# # Connect to SQLite database (creates file if not exists)
# conn = sqlite3.connect("reviews.db")
# cursor = conn.cursor()

# # Create table if not exists
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS reviews (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         code_snippet TEXT,  -- Raw code for retrieval
#         given_code TEXT,    -- Summary + Code (for reference)
#         overall_analysis TEXT -- Context-aware review
#         embedding BLOB  -- Embedding for similarity search
#     )
# """)
# conn.commit()
# # 1. Reset Storage (optional, for clean testing)
# reset_storage()

# # 2. Create some sample review data
# sample_code_1 = "def add(a, b): return a + b"
# sample_review_1 = {
#     "given_code": "This function takes two inputs and returns their sum.\n\nCode:\ndef add(a, b): return a + b",
#     "overall_analysis": "The function is simple and efficient, but lacks type hints."
# }

# sample_code_2 = "def multiply(x, y): return x * y"
# sample_review_2 = {
#     "given_code": "This function multiplies two numbers.\n\nCode:\ndef multiply(x, y): return x * y",
#     "overall_analysis": "The function is fine but lacks input validation."
# }

# # 3. Store the sample reviews in the database
# store_review(sample_code_1, sample_review_1)
# store_review(sample_code_2, sample_review_2)

# # 4. Test retrieval of similar reviews
# retrieved_reviews = retrieve_similar_reviews("def add(x, y): return x + y")
# print("Retrieved Reviews:", retrieved_reviews)

# # 5. Test with another code snippet
# retrieved_reviews = retrieve_similar_reviews("def multiply(a, b): return a * b")
# print("Retrieved Reviews:", retrieved_reviews)

# # cursor.execute("SELECT * FROM reviews")
# # rows = cursor.fetchall()

# # # Print out the rows to verify the reviews are stored
# # print("Stored Reviews:")
# # for row in rows:
# #     print(row)

# # conn.close()


conn = sqlite3.connect("reviews.db")
cursor = conn.cursor()

# Fetch stored embedding
cursor.execute("SELECT embedding FROM code_reviews WHERE id = 1")
stored_embedding_blob = cursor.fetchone()[0]
stored_embedding = np.frombuffer(stored_embedding_blob, dtype=np.float32)

cursor.execute("SELECT review_summary FROM code_reviews WHERE id = 1")
stored_text = cursor.fetchone()[0]
print(f"📜 Stored Text: {stored_text}")
# Recompute embedding
query_text = "The function aims to read a file's content and handle errors gracefully, notably missing files and generic issues. While functional, it lacks robust error handling, security considerations, and scalability for large files. Proper logging and best practices are partially overlooked."
query_embedding = rag_system._get_embedding(query_text)
print(f"📜 Query Text: {query_text}")

# Compare
cosine_sim = np.dot(stored_embedding, query_embedding) / (np.linalg.norm(stored_embedding) * np.linalg.norm(query_embedding))
print("🔍 Manually Computed Cosine Similarity:", cosine_sim)

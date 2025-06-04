
# import sqlite3
# import faiss
# import numpy as np
# import os
# import logging
# import pickle
# import json
# import re
# from azure.ai.inference import ChatCompletionsClient
# from azure.ai.inference.models import SystemMessage
# from azure.ai.inference.models import UserMessage
# from azure.core.credentials import AzureKeyCredential
# from fastapi import HTTPException
# from sentence_transformers import SentenceTransformer


# # Logging Configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)

# class AdvancedCodeReviewRAG:
#     def __init__(self, model_name="BAAI/bge-m3", db_path="reviews.db", index_path="faiss_index.pkl", similarity_threshold=0.7):
#         """Initialize RAG System for Code Review Retrieval"""
#         self.MODEL_NAME = model_name
#         self.DB_PATH = os.path.abspath(db_path)
#         self.INDEX_PATH = os.path.abspath(index_path)
#         self.SIMILARITY_THRESHOLD = similarity_threshold

#         # Load Embedding Model
#         self.model = SentenceTransformer(self.MODEL_NAME)
#         self.embedding_dim = self.model.get_sentence_embedding_dimension()

#         # FAISS Index & ID Mapping
#         self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)
#         self.id_map = []

#         # Setup database and load index
#         self._setup_database()
#         self._load_or_create_index()

#     def _setup_database(self):
#         """Initialize SQLite Database"""
#         conn = sqlite3.connect(self.DB_PATH, check_same_thread=False)
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS code_reviews (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 review_summary TEXT,
#                 embedding BLOB
#             )
#         """)
#         conn.commit()
#         conn.close()
#         logger.info("Database initialized successfully")

#     def _get_embedding(self, text):
#         """Generate embedding for high-level review summary"""
#         #return self.model.encode([text], normalize_embeddings=True)[0].astype(np.float32)
#         embedding = self.model.encode([text])[0].astype(np.float32)
#         return embedding / np.linalg.norm(embedding)

#     def store_review(self, review):
#         """Store Code Review Summary and its Embedding"""
#         try:
#             review_summary = review.get("overall analysis", "").strip()
#             if not review_summary:
#                 logger.warning("Review summary is empty. Skipping storage.")
#                 return None

#             embedding = self._get_embedding(review_summary)

#             # Store in Database
#             conn = sqlite3.connect(self.DB_PATH)
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO code_reviews (review_summary, embedding) VALUES (?, ?)", 
#                            (review_summary, embedding.tobytes()))
#             conn.commit()
#             db_id = cursor.lastrowid
#             conn.close()

#             # Update FAISS Index
#             self.faiss_index.add(embedding.reshape(1, -1))
#             self.id_map.append(db_id)
#             self._save_index()

#             logger.info(f"Review stored successfully. ID: {db_id}")
#             return db_id

#         except Exception as e:
#             logger.error(f"Error storing review: {e}")
#             return None

 

#     def retrieve_similar_reviews(self, code_snippet, top_k=2):
#         """Retrieve Similar Code Reviews Based on Summary using FAISS & Manual Cosine Similarity"""

#         client = ChatCompletionsClient(
#         endpoint="https://models.github.ai/inference",
#         credential=AzureKeyCredential("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"),
#     )
#         # **Step 1: Get Initial Analysis**

#         prompt_initial = f"""
#         You are a senior software architect reviewing the following code snippet.

#         Analyze the given code snippet and provide a single-line **overall analysis** in the following JSON format:

#         **Code Snippet:**
#         {code_snippet}

#         Respond **ONLY in JSON format** as:
#         {{
#             "overall analysis": "<Summarize what the code does and aims to achieve. Provide a concise yet meaningful assessment, highlighting readability, security, performance, best practices, and potential bugs in a structured manner. Use a tone and structure consistent with a more detailed review that will follow.>"
#         }}

#         Ensure that:
#         - The response clearly explains the **functionality of the code** before assessing its quality.
#         - The **key review aspects (readability, security, performance, best practices, potential bugs)** are included naturally.

#       """


#         response_initial = client.complete(
#             messages=[
#                 SystemMessage(""""""),
#                 UserMessage(prompt_initial),
#             ],
#             model="openai/gpt-4o",
#             temperature=1,
#             max_tokens=1024,
#             top_p=1
#         )

#         ai_response_initial = response_initial.choices[0].message.content.strip()

#         # 🔹 Extract JSON for overall analysis
#         json_match = re.search(r"\{.*\}", ai_response_initial, re.DOTALL)
#         if json_match:
#             json_string = json_match.group(0).strip()
#         else:
#             raise HTTPException(status_code=500, detail="Initial AI response did not contain valid JSON.")

#         parsed_initial = json.loads(json_string)
#         overall_analysis = parsed_initial.get("overall analysis", "No analysis available.").strip()

#         if self.faiss_index.ntotal == 0:
#             return "No reviews available."

#         # Generate and Normalize Query Embedding
#         query_embedding = self._get_embedding(overall_analysis)
#         query_embedding = query_embedding / np.linalg.norm(query_embedding)  # 🔥 Ensure Normalization

#         print("\n🔍 Query Embedding:", query_embedding[:5])  # Debugging first 5 values

#         # Connect to Database
#         conn = sqlite3.connect(self.DB_PATH)
#         cursor = conn.cursor()

#         # 🔍 Perform FAISS Search
#         faiss_similarities, indices = self.faiss_index.search(
#             query_embedding.reshape(1, -1), min(top_k, self.faiss_index.ntotal)
#         )

#         similar_reviews = []

#         for faiss_similarity, index in zip(faiss_similarities[0], indices[0]):
#             if index < 0:
#                 continue

#             actual_db_id = self.id_map[index]

#             # 🔹 Fetch Stored Embedding from Database
#             cursor.execute("SELECT embedding FROM code_reviews WHERE id = ?", (actual_db_id,))
#             stored_embedding_blob = cursor.fetchone()[0]
#             stored_embedding = np.frombuffer(stored_embedding_blob, dtype=np.float32)

#             # 🔹 Fetch Stored Text for Verification
#             cursor.execute("SELECT review_summary FROM code_reviews WHERE id = ?", (actual_db_id,))
#             stored_text = cursor.fetchone()[0]
#             print(f"\n📜 Stored Text: {stored_text}")

#             # 🔹 Recompute Embedding for Stored Text
#             recomputed_embedding = self._get_embedding(stored_text)
#             recomputed_embedding = recomputed_embedding / np.linalg.norm(recomputed_embedding)

#             # 🔹 Compute Manual Cosine Similarity
#             manual_cosine_sim = np.dot(stored_embedding, query_embedding) / (
#                 np.linalg.norm(stored_embedding) * np.linalg.norm(query_embedding)
#             )

#             print(f" Query Text: {overall_analysis}")
#             print(f" FAISS Similarity: {faiss_similarity:.4f} | Manual Cosine Similarity: {manual_cosine_sim:.4f}")

#             # Threshold check using manual similarity
#             if manual_cosine_sim < self.SIMILARITY_THRESHOLD:
#                 continue

#             similar_reviews.append(stored_text)

#             if len(similar_reviews) >= top_k:
#                 break

#         conn.close()
#         return similar_reviews if similar_reviews else "No similar review found."

#     def _load_or_create_index(self):
#         """Load or Create FAISS Index"""
#         if os.path.exists(self.INDEX_PATH):
#             try:
#                 with open(self.INDEX_PATH, 'rb') as f:
#                     saved_data = pickle.load(f)
#                     self.faiss_index = saved_data['index']
#                     self.id_map = saved_data['id_map']
#                 logger.info("Loaded FAISS index from disk")
#                 return
#             except Exception as e:
#                 logger.warning(f"Failed to load FAISS index: {e}")

#         self._load_embeddings_from_db()

#     def _load_embeddings_from_db(self):
#         """Load Stored Embeddings into FAISS"""
#         self.faiss_index.reset()
#         self.id_map.clear()

#         conn = sqlite3.connect(self.DB_PATH)
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, embedding FROM code_reviews WHERE embedding IS NOT NULL")
#         rows = cursor.fetchall()

#         embeddings = []
#         for row in rows:
#             db_id, emb_blob = row
#             emb_vector = np.frombuffer(emb_blob, dtype=np.float32)
#             if emb_vector.shape[0] == self.embedding_dim:
#                 embeddings.append(emb_vector)
#                 self.id_map.append(db_id)

#         if embeddings:
#             self.faiss_index.add(np.array(embeddings, dtype=np.float32))
#             logger.info(f"Loaded {len(embeddings)} embeddings into FAISS")

#         conn.close()

#     def _save_index(self):
#         """Persist FAISS Index and ID Mapping"""
#         try:
#             with open(self.INDEX_PATH, 'wb') as f:
#                 pickle.dump({'index': self.faiss_index, 'id_map': self.id_map}, f)
#         except Exception as e:
#             logger.error(f"Failed to save FAISS index: {e}")

#     def close(self):
#         """Save Index Before Closing"""
#         self._save_index()
#         logger.info("RAG system closed")

# # Singleton instance for easy import
# rag_system = AdvancedCodeReviewRAG()

# # Convenience Functions
# def store_review(review):
#     return rag_system.store_review(review)

# def retrieve_similar_reviews(code_snippet, top_k=2):
#     return rag_system.retrieve_similar_reviews(code_snippet, top_k)

import sqlite3
import faiss
import numpy as np
import os
import logging
import pickle
import json
import re
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
from fastapi import HTTPException
from sentence_transformers import SentenceTransformer

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AdvancedCodeReviewRAG:
    def __init__(self, model_name="BAAI/bge-m3", db_path="reviews.db", index_path="faiss_index.pkl", similarity_threshold=0.7):
        """Initialize RAG System for Code Review Retrieval"""
        self.MODEL_NAME = model_name
        self.DB_PATH = os.path.abspath(db_path)
        self.INDEX_PATH = os.path.abspath(index_path)
        self.SIMILARITY_THRESHOLD = similarity_threshold

        # Load Embedding Model
        self.model = SentenceTransformer(self.MODEL_NAME)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        # FAISS Index & ID Mapping
        self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)
        self.id_map = []

        # Setup database and load index
        self._setup_database()
        self._load_or_create_index()

    def _setup_database(self):
        """Initialize SQLite Database"""
        conn = sqlite3.connect(self.DB_PATH, check_same_thread=True)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_summary TEXT,
                embedding BLOB
            )
        """)
        conn.commit()
        conn.close()

    def _get_embedding(self, text):
        """Generate embedding for high-level review summary"""
        embedding = self.model.encode([text])[0].astype(np.float32)
        return embedding / np.linalg.norm(embedding)

    def store_review(self, review):
        """Store Code Review Summary and its Embedding"""
        try:
            review_summary = review.get("overall_analysis", "").strip()
            if not review_summary:
                logger.warning("Review summary is empty. Skipping storage.")
                return None

            embedding = self._get_embedding(review_summary)

            # Store in Database
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO code_reviews (review_summary, embedding) VALUES (?, ?)", 
                           (review_summary, embedding.tobytes()))
            conn.commit()
            db_id = cursor.lastrowid
            conn.close()

            # Update FAISS Index
            self.faiss_index.add(embedding.reshape(1, -1))
            self.id_map.append(db_id)
            self._save_index()

            logger.info(f"Review stored successfully. ID: {db_id}")
            return db_id

        except Exception as e:
            logger.error(f"Error storing review: {e}")
            return None

    def retrieve_similar_reviews(self, code_snippet, top_k=2):
        """Retrieve Similar Code Reviews with FAISS Similarity Scores"""

        client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential("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"),
        )
        # **Step 1: Get Initial Analysis**

        prompt_initial = f"""
        You are a senior software architect reviewing the following code snippet.

        Analyze the provided code snippet and provide a single-line **single-line** overall analysis in JSON format:

        **Code Snippet:**

        {code_snippet}

        Respond **ONLY in JSON format** as:
        {{
            "overall_analysis": "<Summarize what the code does and aims to achieve. Provide a concise assessment, highlighting readability, security, performance, best practices, and potential bugs in a structured manner. Use a tone and structure consistent with a more detailed review that will follow.>"
        }}

        Ensure that:
        - The response clearly explains the **functionality of the code** before assessing its quality.
        - The **key review aspects (readability, security, performance, best practices, potential bugs)** are included naturally.

        """

        response_initial = client.complete(
            messages=[
                SystemMessage(""""""),
                UserMessage(prompt_initial),
            ],
            model="openai/gpt-4o",
            temperature=1,
            max_tokens=1024,
            top_p=1
        )

        ai_response_initial = response_initial.choices[0].message.content.strip()

        # 🔹 Extract JSON for overall analysis
        json_match = re.search(r"\{.*\}", ai_response_initial, re.DOTALL)
        if json_match:
            json_string = json_match.group(0).strip()
        else:
            raise HTTPException(status_code=500, detail="Initial AI response did not contain valid JSON.")

        parsed_initial = json.loads(json_string)
        overall_analysis = parsed_initial.get("overall_analysis", "No analysis available.").strip()

        if self.faiss_index.ntotal == 0:
            return []

        # Generate and Normalize Query Embedding
        query_embedding = self._get_embedding(overall_analysis)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)  # 🔥 Ensure Normalization

        print("\n🔍 Query Embedding:", query_embedding[:5])  # Debugging first 5 values

        # Connect to Database
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        # 🔍 Perform FAISS Search
        faiss_similarities, indices = self.faiss_index.search(
            query_embedding.reshape(1, -1), min(top_k, self.faiss_index.ntotal)
        )

        similar_reviews = []

        for faiss_similarity, index in zip(faiss_similarities[0], indices[0]):
            if index < 0:
                continue

            actual_db_id = self.id_map[index]

            # 🔹 Fetch Stored Embedding from Database
            cursor.execute("SELECT embedding FROM code_reviews WHERE id = ?", (actual_db_id,))
            stored_embedding_blob = cursor.fetchone()
            if not stored_embedding_blob:
                continue
            stored_embedding = np.frombuffer(stored_embedding_blob[0], dtype=np.float32)

            # 🔹 Fetch Stored Text for Verification
            cursor.execute("SELECT review_summary FROM code_reviews WHERE id = ?", (actual_db_id,))
            stored_text = cursor.fetchone()
            if not stored_text:
                continue
            stored_text = stored_text[0]
            print(f"\n📜 Stored Text: {stored_text}")

            # 🔹 Recompute Embedding for Stored Text
            recomputed_embedding = self._get_embedding(stored_text)
            recomputed_embedding = recomputed_embedding / np.linalg.norm(recomputed_embedding)

            # 🔹 Compute Manual Cosine Similarity
            manual_cosine_sim = np.dot(stored_embedding, query_embedding) / (
                np.linalg.norm(stored_embedding) * np.linalg.norm(query_embedding)
            )

            print(f" Query Text: {overall_analysis}")
            print(f" FAISS Similarity: {faiss_similarity:.4f} | Manual Cosine Similarity: {manual_cosine_sim:.4f}")

            # Threshold check using manual similarity
            if manual_cosine_sim < self.SIMILARITY_THRESHOLD:
                continue

            similar_reviews.append({"text": stored_text, "similarity": float(faiss_similarity)})

            if len(similar_reviews) >= top_k:
                break

        conn.close()
        return similar_reviews if similar_reviews else []

    def _load_or_create_index(self):
        """Load or Create FAISS Index"""
        if os.path.exists(self.INDEX_PATH):
            try:
                with open(self.INDEX_PATH, 'rb') as f:
                    saved_data = pickle.load(f)
                    self.faiss_index = saved_data['index']
                    self.id_map = saved_data['id_map']
                logger.info("Loaded FAISS index from disk")
                return
            except Exception as e:
                logger.warning(f"Failed to load FAISS index: {e}")

        self._load_embeddings_from_db()

    def _load_embeddings_from_db(self):
        """Load Stored Embeddings into FAISS"""
        self.faiss_index.reset()
        self.id_map.clear()

        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, embedding FROM code_reviews WHERE embedding IS NOT NULL")
        rows = cursor.fetchall()

        embeddings = []
        for row in rows:
            db_id, emb_blob = row
            emb_vector = np.frombuffer(emb_blob, dtype=np.float32)
            if emb_vector.shape[0] == self.embedding_dim:
                embeddings.append(emb_vector)
                self.id_map.append(db_id)

        if embeddings:
            self.faiss_index.add(np.array(embeddings, dtype=np.float32))
            logger.info(f"Loaded {len(embeddings)} embeddings into FAISS")

        conn.close()

    def _save_index(self):
        """Persist FAISS Index and ID Mapping"""
        try:
            with open(self.INDEX_PATH, 'wb') as f:
                pickle.dump({'index': self.faiss_index, 'id_map': self.id_map}, f)
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {e}")

    def close(self):
        """Save Index Before Closing"""
        self._save_index()
        logger.info("RAG system closed")

# Singleton instance for easy import
rag_system = AdvancedCodeReviewRAG()

# Convenience Functions
def store_review(review):
    return rag_system.store_review(review)

def retrieve_similar_reviews(code_snippet, top_k=2):
    return rag_system.retrieve_similar_reviews(code_snippet, top_k)
import sqlite3
import os


conn = sqlite3.connect("../reviews.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT id, review_summary FROM code_reviews")
rows = cursor.fetchall()

if not rows:
    print("✅ The 'reviews' table is empty.")
else:
    print("❌ Data still exists:", rows)

# conn.close()

# import sqlite3

# # Connect to the database
# conn = sqlite3.connect("../reviews.db")
# cursor = conn.cursor()

# # Drop the existing table (this will delete all stored reviews!)
# cursor.execute("DROP TABLE IF EXISTS reviews")

# # # Recreate the table
# # cursor.execute("""
# # CREATE TABLE reviews (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     code_snippet TEXT,
# #     overall_analysis TEXT,
# #     embedding BLOB
# # )
# # """)

# # Commit and close connection
# # conn.commit()
# # conn.close()

# print("Database reset successfully! The 'reviews' table has been recreated.")

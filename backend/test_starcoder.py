from backend.services.deepseek_api import query_star_coder

sample_code = "def add(a, b): return a+b"  # Example Python code
response = query_star_coder(sample_code)
print(response)

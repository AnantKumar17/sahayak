# test-files/test1.py
def count_words_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return len(file.read().split())
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error occurred: {e}"
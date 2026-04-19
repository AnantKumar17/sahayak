def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return len(file.readlines())
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error occurred: {e}"
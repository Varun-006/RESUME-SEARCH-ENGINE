def read_txt(file_path):
    """
    Read plain text from a .txt file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()

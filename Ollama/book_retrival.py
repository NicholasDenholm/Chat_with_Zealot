import os

# --------------- File loading --------------- #

def load_all_books(book_dir:str) -> list[str]:
    book_paths = []
    for file in os.listdir(book_dir):
        if not file.endswith(".txt"):
            continue
        full_path = os.path.join(book_dir, file)
        book_paths.append(full_path)
    return book_paths

def load_images(data_dir: str) -> list[str]:
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    file_paths = []
    
    for file in os.listdir(data_dir):
        ext = os.path.splitext(file)[1].lower()
        if ext in supported_extensions:
            full_path = os.path.join(data_dir, file)
            file_paths.append(full_path)
    
    return file_paths

def handle_dynamic_file_loading(command: str, current_book: str) -> str:
    """
    Handles the dynamic loading of a new text file if the user issues a 'read: story.txt' command.

    Args:
        command (str): The user's input.
        current_book (str): The current book content.

    Returns:
        str: Updated book content if a file was successfully read, otherwise the original content.
    """
    if command.lower().startswith("read:"):
        new_path = command[5:].strip()
        try:
            new_path = make_book_path(new_path, "book")
            new_content = read_content(new_path)
            print(f"[INFO] Loaded new content from: '{new_path}'")
            return new_content
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
    return current_book

# --------------- Reading --------------- #

def read_content(book_path: str) -> str:
    if not os.path.exists(book_path):
        raise FileNotFoundError(f"Book path not found {book_path}")
    with open(book_path, 'r', encoding='utf8') as f:
        return f.read()

def read_from_list(book_list:list[str]) -> str:
    content = ["===== Start of content =====\n"]

    for book_path in book_list:
        try:
            new_content = read_content(book_path)
            content.append(f"\n--- Start of {os.path.basename(book_path)} ---\n")
            content.append(new_content)
            content.append(f"\n--- End of {os.path.basename(book_path)} ---\n")
        except FileNotFoundError as e:
            print(f"Warning: {e}")

    content.append("===== End of content =====\n")
    return ''.join(content)

# --------------- Path Making --------------- #

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

def make_dir_path(sub_dir:str, dir:str) -> str:
    return os.path.join(sub_dir, dir)

def make_book_path(file_name:str, dir:str) -> str:
    """Concats a file_name and this scripts directory name"""
    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    book_path = os.path.join(base_dir, dir, file_name)     # project-relative file
    return book_path



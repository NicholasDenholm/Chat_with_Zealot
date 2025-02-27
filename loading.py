

class Loading():

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Load only the file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error file at: {self.file_path} not found")
            return None
    
    def load_n_process_data(self):
        """Load and process the file text"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            text = text.lower()  # Convert to lowercase
            text = ''.join([char if char in string.printable else ' ' for char in text])  # Remove non-printable characters
            return text

        except FileNotFoundError:
            print(f"Error: The file at {self.file_path} was not found.")
            return None
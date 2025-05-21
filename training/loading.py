import easygui as g
import sys
import string

class Loading():

    def __init__(self):
        self.file_path = None
        self.output_folder = None

    
    def load_data_box(self):
        file_path = g.fileopenbox(msg="Choose your input text file")

        if file_path:
            #print("Input folder Path:", input_folder)
            self.file_path = file_path
            return file_path
        else:
            print("No file selected. Exiting.")
            sys.exit(0)

    @staticmethod
    def set_output_folder():
        
        output_folder = g.diropenbox(msg="Choose the output folder")

        if output_folder:
            #print("Output Folder:", output_folder)
            return output_folder
        else:
            print("No folder selected. Exiting.")
            sys.exit(0)

    
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
import PyPDF2
import fitz  # PyMuPDF
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import os
from loading import Loading

# ________________________ PDF ________________________

def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")  # Extract text from each page
    return text

def pdf_to_text2(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()  # Extract text from each page
    return text


# ________________________ EPUB ________________________

def epub_to_text(epub_path):
    book = epub.read_epub(epub_path)
    text = ""
    
    print(f"Total items in epub {len(book.get_items())}")

    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.content, "html.parser") # gets rid of html elements
            text += soup.get_text()
    
    # Check if text is being extracted correctly
    if text:
        print("Text extraction successful")
    else:
        print("No text extracted")

    return text

def save_text_to_file(text, output_path):
    # Save the cleaned text to a file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Text saved to {output_path}")

def clean_text(text):
    # Remove unwanted characters or anything that's not textual (like page numbers, footnotes, etc.)
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?;\'"-]', '', text)  # Keep only alphanumeric characters and punctuation
    cleaned_text = cleaned_text.lower()  # Convert to lowercase
    return cleaned_text

def extract_book_name(text):
    # Remove unwanted characters in parenthesis
    book_path = re.sub(r'\((.*?)\)', '', text)  # Noting in brackets

    
    #book_name = re.sub(r'[^/\\]+(?=\.[^/\\]+$|$)', '', book_path)

    # Use regex to extract the last part of the path
    match = re.search(r'[^/\\]+(?=\.[^/\\]+$|$)', book_path)

    if match:
        book_name = match.group(0)
        print(book_name)  # This will print: example_file
        return book_name
    else:
        print("No match found")

    #print(f"Book name is: {book_name} taken from the book path: {book_path}")
    #return book_name

# ______________________________________________________


def run():

    load_isnt = Loading()

    # Define input and output paths
    input_file_path = load_isnt.load_data_box()

    book_name = extract_book_name(input_file_path)
    
    # Folder to store cleaned text files
    output_folder = load_isnt.set_output_folder()

    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Processing PDF
    if input_file_path.endswith(".pdf"):
        print("Processing PDF file...")
        #print(pdf_text[:500])  # Print the first 500 characters of the extracted text
        #pdf_text = pdf_to_text(input_file_path)
        pdf_text = pdf_to_text2(input_file_path)
        cleaned_pdf_text = clean_text(pdf_text)
        #print(cleaned_text[:500])  # Print the first 500 characters of cleaned text
        save_text_to_file(cleaned_pdf_text, os.path.join(output_folder, f"{book_name}.txt"))

    # Processing EPUB
    if input_file_path.endswith(".epub"):
        print("Processing EPUB file...")
        #print(epub_text[:500])  # Print the first 500 characters of the extracted text
        epub_text = epub_to_text(input_file_path)
        cleaned_epub_text = clean_text(epub_text)
        #print(cleaned_text[:500])  # Print the first 500 characters of cleaned text
        save_text_to_file(cleaned_epub_text, os.path.join(output_folder, f"{book_name}.txt"))


if __name__ == "__main__":
    run()
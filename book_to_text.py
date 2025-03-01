# pip install PyMuPDF
# pip install EbookLib

#import PyPDF2
#import fitz  # PyMuPDF
# from ebooklib import epub
# from bs4 import BeautifulSoup
import re
import os

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
    
    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:
            soup = BeautifulSoup(item.content, "html.parser") # gets rid of html elements
            text += soup.get_text()
    
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



def run():

    # Define input and output paths
    input_pdf_path = "your_file.pdf"
    input_epub_path = "your_file.epub"
    output_folder = "training_data"  # Folder to store cleaned text files

    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Processing PDF
    if input_pdf_path.endswith(".pdf"):
        print("Processing PDF file...")
        #print(pdf_text[:500])  # Print the first 500 characters of the extracted text
        pdf_text = pdf_to_text(input_pdf_path)
        cleaned_pdf_text = clean_text(pdf_text)
        #print(cleaned_text[:500])  # Print the first 500 characters of cleaned text
        save_text_to_file(cleaned_pdf_text, os.path.join(output_folder, "pdf_text.txt"))

    # Processing EPUB
    if input_epub_path.endswith(".epub"):
        print("Processing EPUB file...")
        #print(epub_text[:500])  # Print the first 500 characters of the extracted text
        epub_text = epub_to_text(input_epub_path)
        cleaned_epub_text = clean_text(epub_text)
        #print(cleaned_text[:500])  # Print the first 500 characters of cleaned text
        save_text_to_file(cleaned_epub_text, os.path.join(output_folder, "epub_text.txt"))


if __name__ == "__main__":
    run()
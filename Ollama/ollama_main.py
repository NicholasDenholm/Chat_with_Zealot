from PIL import Image
import base64
import io
import os
import requests
import json
from typing import List, Dict

from jinja2 import Template
import ollama
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from personality import setup_named_personality, get_all_personality_names, enum_personality_options
from book_retrival import load_all_books, handle_dynamic_file_loading, get_script_directory, load_images, make_dir_path, read_from_list
from prompt import warhammer_template, rag_template, describe_image_template

### -------------- Setup -------------- ###

def setup_modifiers(test:bool):
    try:
        personalities = get_all_personality_names()
        if test:
            enum_personality_options(personalities)
            option = int(input("Choose from list: "))
            
            choice = personalities[option - 1]
            if choice not in personalities:
                raise ValueError("setuping prompts failed, choice is not in options")
            
            personality = setup_named_personality(choice)
            length, style, emotionality = personality
            print("Using settings:", length, style, emotionality)
        else:
            personalities = get_all_personality_names()
            default_personality = personalities[3]
            #print(f"list: {personalities} \n default: {default_personality}")
            personality = setup_named_personality(default_personality)
    except ValueError as val_err:
        print("Error:", val_err)

    return personality


### -------------- Running the model -------------- ###

def run_model(model, template:str, personality: tuple[str, str, str], content: str) -> None:
    """
    Run an interactive chatbot session with context loaded from a text file.

    Args:
        model: The language model to use in the chain.
        template (str): Prompt template string with placeholders like {book}, {question}, etc.
        personality (tuple): (length, style, emotionality) for prompt control.
        book_path (str): Path to a .txt file containing the book or reference content.
    """
    length, style, emotionality = personality

    # Load book content via helper
    #book_content = read_content(book_path)

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    print("Press q to quit")
    while True:
        try:
            print("\n\n______________________________")
            question = input("You: ")
            print("\n\n")
            if question == 'q':
                break

            result = chain.invoke({
                "book": content,  
                "question": question,
                "length": length,
                "style": style,
                "emotionality": emotionality
            })
            
            print(result)

        except KeyboardInterrupt:
            print("Exiting goodbye...")
            break

### -------------- Images -------------- ###

def describe_image(image_path: str, question: str, length='medium', style='neutral', emotionality='balanced'):
    prompt_template = describe_image_template()
    filled_prompt = Template(prompt_template).render(
        length=length,
        style=style,
        emotionality=emotionality,
        question=question
    )
    print(filled_prompt)
    response = ollama.chat(
        model='llava',
        messages=[
            {'role': 'user', 'content': filled_prompt}
        ],
        images=[image_path]
    )

    return response['message']['content']

def describe_image_with_request(image_path: str, question: str):
    #base64_image = encode_image(image_path)
    base64_image = image_path

    prompt = f"User question: {question}"
    #print("User: ", prompt)

    payload = {
        "model": "llava",
        "messages": [{"role": "user", "content": prompt}],
        "images": [base64_image],
        "stream": True  # Tell Ollama to stream the response
    }

    response = requests.post("http://127.0.0.1:11434/api/chat", json=payload, stream=False)
    if not response.ok:
            return f"Error: {response.status_code} - {response.text}"
    
    

    # Concatenate streamed chunks of JSON into final message
    final_output = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "message" in data and "content" in data["message"]:
                    final_output += data["message"]["content"]
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)

    try:
        data = response.json()
        print("Full JSON response:", json.dumps(data, indent=2))
        return data["message"]["content"]
    except Exception as e:
        return f"Failed to parse response: {e}"

    return final_output

### -------------- Creating Content -------------- ###

#TODO make the model be able to add on to the content it has pre-read
def add_content(question):
    book_content = handle_dynamic_file_loading(question, book_content)
    if question.lower().startswith("read:"):
        return

def create_text_for_bot(retreive_from:str):
    base_dir = get_script_directory()   # gets directory of this script
    target_dir = make_dir_path(retreive_from, base_dir)
    book_list = load_all_books(target_dir)
    content = read_from_list(book_list)
    return content

def create_image_content(retreive_from:str):
    base_dir = get_script_directory()   # gets directory of this script
    target_dir = make_dir_path(base_dir, retreive_from)
    image_list = load_images(target_dir)
    #print(base_dir, target_dir, image_list)
    
    encoded_images = encode_images_from_paths(image_list)
    #return encoded_images
    return image_list

### -------------- Encoding -------------- ###

def encode_image(image: Image.Image) -> str:
    buffered = io.BytesIO()
    #Image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def encode_images_from_paths(file_paths: List[str]) -> Dict[str, str]:
    image_encodings = {}
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}

    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext in image_extensions:
            try:
                with Image.open(path) as img:
                    encoded = encode_image(img)
                    image_encodings[path] = encoded
            except Exception as e:
                print(f"Failed to process {path}: {e}")

    return image_encodings

### -------------- Bot choices -------------- ###

def talk_to_warhammer_bot(test:bool):
    model = OllamaLLM(model="llama3.2")
    personality = setup_modifiers(test=test)
    template = warhammer_template()
    content = ""
    run_model(model, template, personality, content)

def talk_to_code_bot(retreive_from:str, test:bool):
    '''
    ARGS
    retreive_from: directory to look for context text files.
    test: auto sets personality or user can choose.
    '''
    model = OllamaLLM(model="codellama:7b")
    personality = setup_modifiers(test=test)
    template = rag_template()
    content = create_text_for_bot(retreive_from)
    run_model(model, template, personality, content)

def talk_to_image_bot(retrieve_from:str, test:bool):
    model = OllamaLLM(model='llava')
    print(f"Model in use: {model.model}")
    personality = setup_modifiers(test=test)
    template = describe_image_template()
    content = create_image_content(retrieve_from)
    image = content[0]
    

    description = describe_image_with_request(r"Ollama/images/image1.jpg", "What is happening in this image?")
    print(description)
    return

    print("Press q to quit")
    while True:
        try:
            print("\n\n______________________________")
            question = input("You: ")
            print("\n\n")
            if question == 'q': 
                break

            #result = describe_image(image, question)
            result = describe_image_with_request(image, question)
            
            print(result)

        except KeyboardInterrupt:
            print("Exiting goodbye...")
            break
    
    # Example: print one image's base64 string
    #for path, b64 in content.items():
        #print(f"{path} => {b64[:60]}...")
    #run_model(model, template, personality, content)

# --------------- Main --------------- #

def main():

    choice = 3  # Change to switch bots
    test = False

    if choice == 1:
        talk_to_warhammer_bot(test)
    elif choice == 2:
        retreive_from = "book"
        talk_to_code_bot(retreive_from, test)
    elif choice == 3:
        retreive_from = "images"
        talk_to_image_bot(retreive_from, test)
    else:
        print("Error choose 1 or 2")


if __name__ == "__main__":
    main()
    
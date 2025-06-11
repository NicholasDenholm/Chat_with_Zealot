import os
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from personality import setup_named_personality, get_all_personality_names

### -------------- Setup -------------- ###

def setup_prompts(test:bool=False):
    try:
        personalities = get_all_personality_names()
        enum_personality_options(personalities)
        if not (test):
            option = int(input("Choose from list: "))
            
            choice = personalities[option - 1]
            if choice not in personalities:
                raise ValueError("setuping prompts failed, choice is not in options")
            
            personality = setup_named_personality(choice)
            length, style, emotionality = personality
            print("Using settings:", length, style, emotionality)
        else:
            personalities = get_all_personality_names()
            personality = personalities[0]
            personality = setup_named_personality("expert_coder")
    except ValueError as val_err:
        print("Error:", val_err)

    return personality

def enum_personality_options(options:list):
    print("Choose a personality:")
    for i, name in enumerate(options, 1):
        print(f"{i}. {name}")

### -------------- Running the model -------------- ###

def run_model(model, template:str, personality: tuple[str, str, str], book_path: str) -> None:
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
    book_content = load_book_text(book_path)

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
                "book": book_content,  
                "question": question,
                "length": length,
                "style": style,
                "emotionality": emotionality
            })
            
            print(result)

        except KeyboardInterrupt:
            print("Exiting goodbye...")
            break

def load_book_text(book_path: str) -> str:
    if not os.path.exists(book_path):
        raise FileNotFoundError(f"Book path not found {book_path}")
    
    with open(book_path, 'r', encoding='utf8') as f:
        return f.read()


# --------------- Templates --------------- #

def warhammer_template() -> str:
    template = """
    You are a religious zealot from the Warhammer 40K universe.

    Answer the following question as a devout zealot. Customize your response according to:

        - **Desired Length**: {length}
        - **Style**: {style}
        - **Emotional Tone**: {emotionality}

    Question: {question}
    """
    return template

def rag_template() -> str:
    template = """
    You are an AI trained on the following book content:

    {book}

    Answer the user's question based on the content above. Be {style}, write with {emotionality} emotionality, and keep it {length} in length.

    User: {question}
    AI:
    """
    return template


# --------------- Main --------------- #

def main():

    #model = OllamaLLM(model="llama3.2")
    model = OllamaLLM(model="codellama:7b")
    personality = setup_prompts()


    file_name = "book.txt"
    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    book_path = os.path.join(base_dir, "book", file_name)       # project-relative file
    
    #template = warhammer_template()
    template = rag_template()

    run_model(model, template, personality, book_path)

if __name__ == "__main__":
    main()
    
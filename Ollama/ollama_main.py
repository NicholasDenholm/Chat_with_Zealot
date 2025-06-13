import os
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from personality import setup_named_personality, get_all_personality_names, enum_personality_options
from book_retrival import load_all_books, handle_dynamic_file_loading, get_script_directory, read_content, make_dir_path, read_from_list
from prompt import warhammer_template, rag_template 

### -------------- Setup -------------- ###

def setup_modifiers(test:bool=False):
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


### -------------- Running the model -------------- ###

#TODO make the model be able to add on to the content it has pre-read
def add_content(question):
    book_content = handle_dynamic_file_loading(question, book_content)
    if question.lower().startswith("read:"):
        return


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


# --------------- Main --------------- #

def main():

    #model = OllamaLLM(model="llama3.2")
    model = OllamaLLM(model="codellama:7b")
    personality = setup_modifiers()

    look_in = "book"                    # Directory to look for txt files in
    base_dir = get_script_directory()   # gets directory of this script
    target_dir = make_dir_path(look_in, base_dir)
    book_list = load_all_books(target_dir)
    
    content = read_from_list(book_list)
    
    #template = warhammer_template()
    template = rag_template()

    run_model(model, template, personality, content)

if __name__ == "__main__":
    main()
    
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

### -------------- Setup -------------- ###

def setup_prompts(test:bool=False):
    
    try:
        if not (test):
            option = int(input("Choose personality (1: fanatic, 2: preacher, 3: sermon-lite): "))
            personality = set_personality(option)
            length, style, emotionality = personality
            print("Using settings:", length, style, emotionality)
        else:
            personality = set_personality(1)
    except ValueError as val_err:
        print("Error:", val_err)

    return personality

def set_personality(option:int) -> tuple[str, str, str]:
    '''
    Arguments: recieves option: 1 - 3 corresponding to different personas
    1 | fanatic : medium aggressive and wrathful
    2 | preacher : long formal and passionate
    3 | sermon-lite : short poetic and calm

    returns a tuple of (length, style, emotionality)
    '''
    presets = {1: {"length": "medium", "style": "aggressive", "emotionality": "wrathful"}, 
                2: {"length": "long", "style": "formal", "emotionality": "passionate"},
                3: {"length": "short", "style": "poetic", "emotionality": "calm"}
    }
    if option not in presets:
        raise ValueError("Invalid input error, Choose 1 (fanatic), 2 (preacher), or 3 (sermon-lite)")

    info = presets[option]

    return info["length"], info["style"], info["emotionality"]  

### -------------- Running the model -------------- ###

def run_model(model, template:str, personality: tuple[str, str, str]) -> None:

    length, style, emotionality = personality

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
                "book": [],  # Replace this with real context (text/a sting) if needed
                "question": question,
                "length": length,
                "style": style,
                "emotionality": emotionality
            })
            
            print(result)

        except KeyboardInterrupt:
            print("Exiting goodbye...")
            break


def main():

    #model = OllamaLLM(model="llama3.2")
    model = OllamaLLM(model="codellama:7b")
    personality = setup_prompts()
    template = """
    You are a religious zealot from the Warhammer 40K universe.

    Answer the following question as a devout zealot. Customize your response according to:

        - **Desired Length**: {length}
        - **Style**: {style}
        - **Emotional Tone**: {emotionality}

    Question: {question}
    """
    
    run_model(model, template, personality)

if __name__ == "__main__":
    main()
    
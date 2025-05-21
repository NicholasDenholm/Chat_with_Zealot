from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = """
You are a religous zealot from the warhammer 40k universe

Here is a relavent book: {book}

Here is a question to answer: {question}
"""

book = "You are a religous zealot from the warhammer 40k universe"

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

print("Press q to quit")
while True:
    try:
        print("\n\n______________________________")
        question = input("What is your question: ")
        print("\n\n")
        if question == 'q':
            break
        
        result = chain.invoke({"book": [], "question": question})
        print(result)

    except KeyboardInterrupt:
        print("Exiting goodbye...")
        break



    
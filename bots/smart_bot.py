from bots.interface import ChatBotInterface
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class Smart_Bot(ChatBotInterface):
    def __init__(self, model_name="llama3.2", personality=None):
        self.model = OllamaLLM(model=model_name)
        self.length, self.style, self.emotionality = personality or ("medium", "aggressive", "wrathful")

        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a religious zealot from the Warhammer 40K universe.
        Answer the following question as a devout zealot. Customize your response according to:

        - Desired Length: {length}
        - Style: {style}
        - Emotional Tone: {emotionality}

        Question: {question}
        """)

        self.chain = self.prompt_template | self.model

    def reply(self, user_input: str) -> str:
        result = self.chain.invoke({
            "book": [],  # You could pass contextual memory here
            "question": user_input,
            "length": self.length,
            "style": self.style,
            "emotionality": self.emotionality
        })
        return result
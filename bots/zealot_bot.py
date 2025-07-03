from bots.interface import ChatBotInterface
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from Ollama.personality import get_personality_by_name, get_all_personality_names, resolve_personality

class Zealot_Bot(ChatBotInterface):
    def __init__(self, model_name:str, personality:str):
        self.model_name = model_name
        self.model = OllamaLLM(model=model_name)

        self.length, self.style, self.emotionality, personality_name = resolve_personality(personality, "fanatic")
        # Only set if resolved
        self.personality = personality_name

        # TODO make this take from Ollama/prompts warhammer function
        self.prompt_template = ChatPromptTemplate.from_template(f"""
        You are a religious zealot from the Warhammer 40K universe.
        Answer the following using a personality of {personality_name}. 
                                                                
        Customize your response according to:
        - Desired Length: {{length}}
        - Style: {{style}}
        - Emotional Tone: {{emotionality}}

        Question: {{question}}
        """)

        self.chain = self.prompt_template | self.model

    def resolve_personality(self, personality_input) -> tuple[str, str, str, str]:
        """
        Resolves a personality input (string or tuple) to a standard format:
        (length, style, emotionality, personality_name)

        Falls back to the first defined personality if input is invalid.
        """
        # Handle tuple
        if isinstance(personality_input, tuple) and len(personality_input) == 3:
            length, style, emotionality = personality_input
            return length, style, emotionality, "custom"

        # Handle name string
        elif isinstance(personality_input, str):
            try:
                length, style, emotionality = get_personality_by_name(personality_input)
                return length, style, emotionality, personality_input
            except ValueError:
                print(f"[Warning] Unknown personality '{personality_input}'")

        # Fallback to fanatic
        fallback_name = 'fanatic'
        length, style, emotionality = get_personality_by_name('fanatic')
        print(f"[Fallback] Using default personality '{fallback_name}'.")
        return length, style, emotionality, fallback_name

    def reply(self, user_input: str) -> str:
        result = self.chain.invoke({
            "book": [],  # You could pass contextual memory here
            "question": user_input,
            "length": self.length,
            "style": self.style,
            "emotionality": self.emotionality
        })
        return result
    
    def modify_chat_history(self, user_input:str, chat_history_ids:list, max_memory:int):
        # Initialize or use existing chat history
        if chat_history_ids is None:
            chat_history = []
        else:
            print("Appending chat_history_ids..")
            chat_history = chat_history_ids
        
        # Add user message to history
        chat_history.append({'role': 'user', 'content': user_input})

        if len(chat_history) > max_memory:
            chat_history = chat_history[-max_memory:]

        return chat_history

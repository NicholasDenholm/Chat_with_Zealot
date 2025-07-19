from bots.interface import ChatBotInterface
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from Ollama.personality import get_personality_by_name, get_all_personality_names, resolve_personality
from Ollama.prompt import warhammer_template

class Zealot_Bot():
    def __init__(self, model_name:str, personality:str):
        self.model_name = model_name
        self.model = OllamaLLM(model=model_name)

        self.length, self.style, self.emotionality, personality_name = resolve_personality(personality, "fanatic")
        # Only set if resolved
        self.personality = personality_name

        self.prompt_template = ChatPromptTemplate.from_template(warhammer_template())
        '''
        self.prompt_template = ChatPromptTemplate.from_template(f"""
        You are a religious zealot from the Warhammer 40K universe.
        Answer the following using a personality of {personality_name}. 
                                                                
        Customize your response according to:
        - Desired Length: {{length}}
        - Style: {{style}}
        - Emotional Tone: {{emotionality}}

        Question: {{question}}
        """)
        '''
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

    def reply_directly(self, user_input: str) -> str:
        # Replies without looking at past conversation history
        result = self.chain.invoke({
            "book": [],  # You could pass contextual memory here
            "question": user_input,
            "length": self.length,
            "style": self.style,
            "emotionality": self.emotionality
        })
        return result
    
    def reply(self, user_input: str, chat_history: list = None) -> str:
        # Format chat history for the book parameter
        book_context = []
        if chat_history:
            for msg in chat_history:
                # Convert the chat history into a readable format for context
                role = "User" if msg['role'] == 'user' else "Assistant"
                book_context.append(f"{role}: {msg['content']}")
        
        #print("\nBook content:", book_context, "\n")

        result = self.chain.invoke({
            "book": book_context,  # Pass the conversation history as context
            "question": user_input,
            "length": self.length,
            "style": self.style,
            "emotionality": self.emotionality
        })
        return result
    
    def add_user_message(self, user_text: str, chat_history_ids: list, max_memory: int):
        """Add user message to chat history and trim if needed"""
        # Initialize if None
        if chat_history_ids is None:
            chat_history_ids = []
            #chat_history_ids.clear()
            #chat_history_ids.extend([])
        
        # Add user message to history
        chat_history_ids.append({'role': 'user', 'content': user_text})
        
        # Trim history if it exceeds max memory
        if len(chat_history_ids) > max_memory:
            # Keep only the last max_memory messages
            chat_history_ids[:] = chat_history_ids[-max_memory:]

    def add_bot_message(self, bot_text: str, chat_history_ids: list, max_memory: int):
        """Add bot response to chat history and trim if needed"""
        # Initialize if None
        if chat_history_ids is None:
            chat_history_ids = []
            #chat_history_ids.clear()
            #chat_history_ids.extend([])
        
        # Add bot message to history
        chat_history_ids.append({'role': 'assistant', 'content': bot_text})
        
        # Trim history if it exceeds max memory
        if len(chat_history_ids) > max_memory:
            # Keep only the last max_memory messages
            chat_history_ids[:] = chat_history_ids[-max_memory:]

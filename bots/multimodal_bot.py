from PIL import Image
import base64
import io

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from Ollama.personality import get_personality_by_name, get_all_personality_names, resolve_personality
from bots.interface import ChatBotInterface

import torch
from transformers import LlavaProcessor, LlavaForConditionalGeneration


class Multimodal_Bot(ChatBotInterface):
    def __init__(self, model_name:str, personality:str):
        self.model_name = model_name
        self.model = OllamaLLM(model=model_name)

        self.length, self.style, self.emotionality, personality_name = resolve_personality(personality, "fanatic")
        # Only set if resolved
        self.personality = personality_name

        self.prompt_template = ChatPromptTemplate.from_template(f"""
        You must describe this image by using a personality of {personality_name}. 
                                                                
        Customize your response according to:
        - Desired Length: {{length}}
        - Style: {{style}}
        - Emotional Tone: {{emotionality}}

        image: {{image}}
        """)

        self.chain = self.prompt_template | self.model

    def encode_image(self, image: Image.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def reply(self, user_input: str, image_path:str) -> str:
        image = Image.open(image_path).convert("RGB")
        image_b64 = self.encode_image(image)

        inputs = {
            "length": self.length,
            "style": self.style,
            "emotionality": self.emotionality,
            "image": image_b64,  # Assume your model supports raw image bytes
            "user_input": user_input
        }

        return self.chain.invoke(inputs)

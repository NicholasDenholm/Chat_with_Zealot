from typing import Optional
from PIL import Image

class ChatBotInterface:
    def reply(self, user_input: str, image: Optional[Image.Image] = None) -> str:
        """Generate a response given a user input"""
        raise NotImplementedError("Subclasses must implement this method.")
    
'''
# Maybe seperate multimodal and chat bots fully?
# --> if so change class inheritance for multimodal_bot.py

class MultimodalBotInterface:
    def reply(self, user_input: str, image: Optional[Image.Image] = None) -> str:
        raise NotImplementedError("Subclasses must implement this method.")

'''


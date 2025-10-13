#from interface import ChatBotInterface
from prebuilt.app.chat_bot import chat_with_speech, init_chat_state

class Dumb_Bot():
    def __init__(self, model):
        self.model_name = model
        self.type = "dumb_bot"
        self.state = init_chat_state(model)

    def reply_from_dictionary(self, context:dict):
        # Grab all values that look like strings or have a `.message.content`
        texts = []

        for value in context.values():
            if hasattr(value, "message") and hasattr(value.message, "content"):
                texts.append(value.message.content)
            elif isinstance(value, str):
                texts.append(value)

        combined_input = "\n".join(texts)
        return chat_with_speech(combined_input, self.state)
        #user_request = context.keys()
        #return chat_with_speech(user_request, self.state)
 
    def reply(self, user_input: str) -> str:
        return chat_with_speech(user_input, self.state)
    
    def to_dict(self):
        return {
            "bot_type": self.type,
            "model_name": self.model_name  
        }
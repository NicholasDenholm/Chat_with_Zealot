from bots.interface import ChatBotInterface
from prebuilt.app.chat_bot import chat_with_speech, init_chat_state

class Dumb_Bot(ChatBotInterface):
    def __init__(self, model):
        self.model_name = model
        self.type = "dumb_bot"
        self.state = init_chat_state(model)

    def reply(self, user_input: str) -> str:
        return chat_with_speech(user_input, self.state)
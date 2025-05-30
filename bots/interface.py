class ChatBotInterface:
    def reply(self, user_input: str) -> str:
        """Generate a response given a user input"""
        raise NotImplementedError("Subclasses must implement this method.")


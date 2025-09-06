import dumb_bot, smart_bot, whisper_bot, multimodal_bot
import bots

class Coordinator:
    def __init__(self, vision_bot=None, dumb_bot=None, smart_bot=None):
        self.vision_bot = vision_bot
        self.dumb_bot = dumb_bot
        self.smart_bot = smart_bot

    def process_input(self, user_text=None, image=None):
        responses = {}

        # Step 1: Vision Analysis
        if image and self.vision_bot:
            vision_result = self.vision_bot.reply(user_input=user_text, image=image)
            responses["vision"] = vision_result
        else:
            vision_result = ""

        # Step 2: Dumb Reaction
        if self.dumb_bot:
            dumb_input = vision_result if image else user_text
            dumb_response = self.dumb_bot.reply(dumb_input)
            responses["dumb"] = dumb_response
        else:
            dumb_response = ""

        # Step 3: Smart Reasoning
        if self.smart_bot:
            combined_input = f"""
            User Input: {user_text}
            Vision Bot: {vision_result}
            Dumb Bot: {dumb_response}
            """
            smart_response = self.smart_bot.reply(combined_input)
            responses["smart"] = smart_response

        return responses

def main():
    
    smart = bots.build_smart_bot()
    dumb = dumb_bot.Dumb_Bot("microsoft/DialoGPT-large")
    sound = bots.build_whisper_bot()
    vision = bots.build_vision_bot()


    Coordinator()

if __name__ == "__main__":
    main()

import openai
from PIL import Image
import base64
import io
from bots.interface import ChatBotInterface

class Multimodal_Bot(ChatBotInterface):
    def __init__(self, personality: Union[str, tuple] = "fanatic"):
        self.length, self.style, self.emotionality = process_personality_input(personality)
        self.system_prompt = (
            "You are a multimodal assistant with the persona of a Warhammer zealot.\n"
            f"- Length: {self.length}\n"
            f"- Style: {self.style}\n"
            f"- Emotionality: {self.emotionality}\n"
            "Interpret images and text with religious fervor."
        )

    def encode_image(self, image: Image.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def reply(self, user_input: str, image: Optional[Image.Image] = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}]
        
        if image:
            base64_image = self.encode_image(image)
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
                tools=[],
                tool_choice=None,
                images=[
                    {
                        "image": {
                            "data": base64_image,
                            "type": "base64"
                        },
                        "role": "user"
                    }
                ]
            )
        else:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
            )

        return response.choices[0].message.content.strip()

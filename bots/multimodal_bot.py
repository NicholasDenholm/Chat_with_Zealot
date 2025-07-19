#from bots.interface import ChatBotInterface
import ollama
import os

class Multimodal_Bot():
    def __init__(self, model_name: str, personality: str):
        self.model_name = model_name
        self.personality = personality  

    def reply(self, user_request:str, image_path:str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        result = ollama.chat(
            model = self.model_name,
            messages=[
                {'role': 'user',
                'content': user_request,
                'images': [image_path]
                }
            ]

        ) 
        return result

        
def build_multimodal_bot(model_name: str, personality: str):
    return Multimodal_Bot(model_name=model_name, personality=personality)

def get_user_request_array() -> list:
    return [
        "Describe this image:",
        "Count how many objects are in this image:",
        "Provide 5 keywords describing this image (seperated by commas)",
        "You are a helpful assistant, answer the question with a short, poetic style, and clam emotional tone. Question: Can you describe this image?"
    ]

def main():

    request_array = get_user_request_array()
    user_request = request_array[2]
    image_path = os.path.join("Ollama", "images", "image4.jpg")

    bot = build_multimodal_bot(model_name='llava', personality="nice_person")

    try:
        response = bot.reply(user_request, image_path)
        print("\n------------------")
        print(response['message']['content'])
        print("------------------\n")
    except Exception as error:
        print("Error as: {error}")



if __name__ == "__main__":
    main()


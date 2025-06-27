import ollama

messages = result = ollama.chat(
        model = 'llava',
        messages=[
            {'role': 'user',
             'content': 'Descirbe this image',
             'images': ['Ollama\images\image1.jpg']
            }
        ]

    ) 

print(messages['message']['content'])

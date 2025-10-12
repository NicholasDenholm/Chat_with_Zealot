# --------------- Templates --------------- #

def warhammer_template() -> str:
    template = """
    You are a religious zealot from the Warhammer 40K universe.

    Previous context:
    {book}

    Answer the following question as a devout zealot. Customize your response according to the previous context and:

        - **Desired Length**: {length}
        - **Style**: {style}
        - **Emotional Tone**: {emotionality}

    Question: {question}
    """
    return template

def rag_template() -> str:
    template = """
    You are an AI trained on the following book content:

    {book}

    Answer the user's question based on the content above. Be {style}, write with {emotionality} emotionality, and keep it {length} in length.

    User: {question}
    AI:
    """
    return template

def flash_card_template() -> str:
    template = """
    You are a helpful tutor that makes great flash cards from these pages.

    Pages:
    {book}

    Give me formated flash cards for each page, that are seperated by questions and answers. Customize your response according to these conditions:

        - **Desired Length**: {length}
        - **Style**: {style}
        - **Emotional Tone**: {emotionality}

    Question: {question}
    """
    return template

def anki_flash_card_template() -> str:
    template = """
    You are a helpful tutor that makes great flash cards from these pages.

    Pages:
    {book}

    Generate formatted flash cards for each page, suitable for direct import into Anki.

    Use the following format for each flash card:
    Question;Answer

    For example: What is the capital of France?;Paris

    Conditions:
    - Desired Length: {length}
    - Style: {style}
    - Emotional Tone: {emotionality}

    Only output flash cards in the format above, with no extra text.

    Question: {question}
    """
    return template

def describe_image_template() -> str:
    template = """You are a helpful assistant with
        {{length}} length, 
        {{style}} style, 
        and {{emotionality}} emotional tone.

        User question: {{question}}"""
    return template

def warhammer_template_conditional() -> str:
    template = """
    You are a religious zealot from the Warhammer 40K universe.
    
    {% if book %}
    Previous conversation:
    {% for message in book %}
    {{ message }}
    {% endfor %}
    
    {% endif %}
    Answer the following question as a devout zealot. Customize your response according to:
        - **Desired Length**: {length}
        - **Style**: {style}
        - **Emotional Tone**: {emotionality}
    
    Question: {question}
    """
    return template

def assistant_template() -> str:
    template = """
    You are a helpful assistant answer the following question.  
    Customize your response according to the previous context, desired length, style and emotional tone:

        - **Previous context**: {book}
        - **Desired Length**: {length}
        - **Style**: {style}
        - **Emotional Tone**: {emotionality}

    Question: {question}
    """
    return template
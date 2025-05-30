def setup_prompts(test:bool=False):
    
    try:
        if not (test):
            option = int(input("Choose personality (1: fanatic, 2: preacher, 3: sermon-lite): "))
            personality = set_personality(option)
            length, style, emotionality = personality
            print("Using settings:", length, style, emotionality)
        else:
            personality = set_personality(3)
    except ValueError as val_err:
        print("Error:", val_err)

    return personality

def set_personality(option:int) -> tuple[str, str, str]:
    '''
    Arguments: recieves option: 1 - 3 corresponding to different personas
    1 | fanatic : medium aggressive and wrathful
    2 | preacher : long formal and passionate
    3 | sermon-lite : short poetic and calm

    returns a tuple of (length, style, emotionality)
    '''
    presets = {1: {"length": "medium", "style": "aggressive", "emotionality": "wrathful"}, 
                2: {"length": "long", "style": "formal", "emotionality": "passionate"},
                3: {"length": "short", "style": "poetic", "emotionality": "calm"}
    }
    if option not in presets:
        raise ValueError("Invalid input error, Choose 1 (fanatic), 2 (preacher), or 3 (sermon-lite)")

    info = presets[option]

    return info["length"], info["style"], info["emotionality"]  
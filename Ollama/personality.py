# ----------------- Presets ----------------- #

def personality_presets() -> dict[str, tuple[str, str, str]]:
    return {
        "fanatic": ("medium", "aggressive", "wrathful"),
        "preacher": ("long", "formal", "passionate"),
        "sermon-lite": ("short", "poetic", "calm"),
        "nice_person": ("medium", "friendly", "cheerful"),
        "expert_coder": ("long", "technical", "neutral"),
        "short_answers": ("short", "blunt", "flat"),
        "mean_person": ("medium", "rude", "irritable"),
    }

def validate_personality_name(personality: str, fallback: str = "nice_person") -> str:
    """
    Checks if the given personality name exists. If not, returns the fallback.
    """
    available = get_all_personality_names()
    if personality not in available:
        print(f"[Warning] Personality '{personality}' not found. Falling back to '{fallback}'.")
        return fallback
    return personality


# ----------------- Setup ----------------- #


def setup_named_personality(name:str, test:bool = False) -> tuple[str, str, str]:
    """Setup a bot's personality by string label, like 'fanatic', 'preacher', 'sermon-lite', or 'nice_person'."""
    try:
        if not test:
            personality = get_personality_by_name(name)
            print(f"Using settings for '{name}':", personality)
        else:
            personality = get_personality_by_name("sermon-lite")
    except ValueError as e:
        print("Error seting up personality:", e)
        return None

    return personality


def setup_prompts(test:bool=False):
    """Setup bot's personality by inputted integer option"""
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

# ----------------- Setters ----------------- #

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


# ----------------- Getters ----------------- #


def get_all_personality_names() -> list[str]:
    """Returns a list of all available personality names."""
    return list(personality_presets().keys())

def get_all_personality_names() -> list[str]:
    """Returns a list of all available personality names."""
    return list(personality_presets().keys())

def get_personality_by_name(name: str) -> tuple[str, str, str]:
    presets = personality_presets()
    print(type(name))
    name = name.lower()
    print(name, "\n-------\n")

    if name not in presets:
        raise ValueError(f"Invalid personality name: {name}. Available: {', '.join(presets)}")

    return presets[name]
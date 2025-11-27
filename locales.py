

LOCALES = {}

LOCALES["en"] = {
    "position": "position",
    "car": "car",
    "notime": "no time",
    "noone": "noone",
    "leader": "leader"
}

LOCALES["es"] = {
    "position": "posición",
    "car": "coche",
    "notime": "sin tiempo",
    "noone": "nadie",
    "leader": "líder"
}

def L(word, lang = "en"):
    if lang in LOCALES:
        return LOCALES[lang].get(word)
    else:
        return word
    
def get_locales(lang = "en"):
    if lang in LOCALES:
        return LOCALES[lang]


LOCALES = {}

LOCALES["en"] = {
    "behind": "behind",
    "front": "front"
}

LOCALES["es"] = {
    "behind": "detrás",
    "front": "delante"
}

def L(word, lang = "en"):
    if lang in LOCALES:
        return LOCALES[lang].get(word)
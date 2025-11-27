from num2words import num2words
from locales import L, get_locales

REPLACES = []

def init_replaces(lang="es"):
    for i in range(0,999):
        REPLACES.append({ "text": num2words(i, lang=lang), "replace": str(i)})
        REPLACES.append({ "text": "{} {}".format(L("position", lang=lang), num2words(i, lang=lang)), "replace": "P"+str(i)})
    REPLACES.sort(key = lambda x: len(x["text"]), reverse=True)
    REPLACES.append({ "text": L("leader", lang=lang), "replace": "P1"})
    
# TODO
# Añadir tokes de iracing

def replace(str):
    if not str:
        return None
    
    for s in REPLACES:
        str = str.replace(s["text"], s["replace"])
    return str


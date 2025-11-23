from num2words import num2words

REPLACES = {}

def init_parser():
    for i in range(0,999):
        REPLACES[num2words(i, lang="es")] = str(i)

# TODO
# Añadir tokes de iracing

def replace(str):
    if str in REPLACES:
        return REPLACES[str]
    else:
        return str


from recognizer import VoskRecognizer
from overlay import Overlay
from ahk import AHK
from PyQt5.QtWidgets import QApplication
import time, signal
import json
import re
import os
import subprocess
from deep_translator import GoogleTranslator
import pyttsx3
from data import get_data

ONLY_IRACING = False

################################################################################
# Loading configuration from config.json
################################################################################

if not os.path.exists('config.json'):
    print("Configuration not found. (see README.md)")
    exit()

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

driver_language = config.get("DriverLanguage", "en")
radio_language  = config.get("DefaultRadioLanguage", "en")
ahk_path        = config.get("AhkPath")
auto_hide_idle  = config.get("AutoHideIdle", 0)
draw_overlay    = config.get("Overlay", 1)
vosk_model_path = config.get("VoskModelPath", "model")
free_radio_activator = config.get("FreeRadioButton")
engineer_activator = config.get("EngineerButton")

################################################################################
#   I N I T
################################################################################

# Requirement: ahk setup
try:
    ahk = AHK(executable_path=ahk_path)
except:
    try:
        ahk = AHK(version="v2", executable_path=ahk_path)
    except:
        print("AHK not found. Shutting down. (see README.md)")
        exit()

# Requirement: vosk recognizer model
vosk = VoskRecognizer(model=vosk_model_path)

# app and overlay
app = QApplication([])
overlay = Overlay(autohide=auto_hide_idle) if draw_overlay else None

# getting a phrase from mic
def getSpeech():
    if overlay: overlay.listeningMode()
    speech = vosk.recognizeMic()
    if overlay: overlay.waitingMode()
    if speech and len(speech) > 0: return speech

def speak(str):
    speaker = pyttsx3.init()
    speaker.say(str)
    speaker.runAndWait()
    speaker.stop()

################################################################################
#   F R E E    R A D I O
################################################################################

# iRacing chat message sending
def chat(str, target=radio_language):
    if driver_language and driver_language != target:
        str = GoogleTranslator(source=driver_language, target=target).translate(str)
    print("CHATING: " + str)
    ahk.send("{^}")
    time.sleep(0.1)
    ahk.send("{Escape}")
    time.sleep(0.1)
    ahk.send("{t}")
    time.sleep(0.1)
    ahk.send_raw("{}".format(str))
    ahk.send("{Enter}")
    time.sleep(0.3)
    ahk.send("{Escape}")

# free radio activation
def useRadio():
    if not ONLY_IRACING or ahk.active_window.get_process_name() == "iRacingSim64DX11.exe":
        if overlay: overlay.listeningMode()
        speech = vosk.recognizeMic()
        #print(speech, replace(speech))
        if speech and len(speech) > 0: chat(replace(speech), target = radio_language)
        if overlay: overlay.waitingMode()

################################################################################
#   E N G I N E E R
################################################################################

from replaces import *

init_replaces(lang=driver_language)

ENGINEER_COMMANDS = config["EngineerCommands"]
VALID_COMMAND_TYPES = ("chat", "keypress", "run", "say")

# Populating commands from config.json
for item in ENGINEER_COMMANDS:
    if not "command" in item or not "type" in item or not item["type"] in VALID_COMMAND_TYPES:
        print("Bad Engineer command. Exiting")
        print(item)
        exit()

# Adding translator commnads
TRANSLATIONS = config.get("EngineerTranslations", {})
for lang in TRANSLATIONS:
    acro = TRANSLATIONS[lang]
    ENGINEER_COMMANDS.append({
        "command": "^{} (.*)".format(lang),
        "type": "chat",
        "target": acro,
        "msg": "\\1"
    })
#print(ENGINEER_COMMANDS)

def send_keys(keys = ""):
    print("SENDING KEYS:" + keys)
    ahk.send(keys)

def callEngineer():
    speech = getSpeech()
    if not speech:
        return
    speech = replace(speech)
    for item in ENGINEER_COMMANDS:
        command = item["command"]
        r = re.search(command, speech)
        if not r: continue
        print("MATCHED: " + command)
        dispatcher = item["type"]
        if dispatcher == "chat" and "msg" in item:
            try:
                chat(re.sub(command, item["msg"], speech).format(**get_data()), target=item.get("target"))
            except:
                print("Data not ready.")
        elif dispatcher == "keypress" and "keys" in item:
            send_keys(item["keys"])
        elif dispatcher == "run" and "path" in item:
            subprocess.call(item["path"])
        elif dispatcher == "say" and "msg" in item:
            print(re.sub(command, item["msg"], speech))
            try:
                speak(re.sub(command, item["msg"], speech).format(**get_data()))
            except:
                print("Data not ready.")


ahk.add_hotkey(free_radio_activator, callback=useRadio)
ahk.add_hotkey(engineer_activator, callback=callEngineer)

ahk.start_hotkeys()

# ctrl+c catch
signal.signal(signal.SIGINT, signal.SIG_DFL)

# run (may be we dont need it with no overlay)
app.exec()
from recognizer import VoskRecognizer
from overlay import Overlay
from ahk import AHK
from PyQt5.QtWidgets import QApplication
import time, signal
import json

# loading configuration
with open('config.json', 'r') as file:
    config = json.load(file)

ahk_path        = config.get("AhkPath")
auto_hide_idle  = config.get("AutoHideIdle")
draw_overlay    = config.get("Overlay")
vosk_model_path = config.get("VoskModelPath")
radio_activator = config.get("RadioButton")

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

# iRacing chat message sending
def chat(str):
    ahk.send("{^}")
    ahk.send("{Escape}")
    ahk.send("{t}")
    time.sleep(0.1)
    ahk.send_raw("{}".format(str))
    ahk.send("{Enter}")
    time.sleep(0.1)
    ahk.send("{Escape}")

# radio activation (only on iRacing)
def useRadio():
    # if ahk.active_window.get_process_name() == "iRacingSim64DX11.exe":
        if overlay: overlay.listeningMode()
        speech = vosk.recognizeMic()
        if speech and len(speech) > 0: chat(speech)
        if overlay: overlay.waitingMode()

ahk.add_hotkey(radio_activator, callback=useRadio)
ahk.start_hotkeys()

# ctrl+c catch
signal.signal(signal.SIGINT, signal.SIG_DFL)

# run (may be we dont need it with no overlay)
app.exec()
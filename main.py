from recognizer import VoskRecognizer
from overlay import Overlay
from ahk import AHK
from PyQt5.QtWidgets import QApplication

import time, signal

import json

with open('config.json', 'r') as file:
    config = json.load(file)

# app and overlay
app = QApplication([])
overlay = Overlay(autohide=config["AutoHideIdle"]) if config["Overlay"] else None

# recognizer setup
r = VoskRecognizer()
r.start()

# ahk setup
try:
    ahk = AHK()
except:
    ahk = AHK(version="v2")

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
    if ahk.active_window.get_process_name() == "iRacingSim64DX11.exe":
        if overlay: overlay.listeningMode()
        speech = r.recognizeMic()
        if speech and len(speech) > 0: chat(speech)
        if overlay: overlay.waitingMode()

ahk.add_hotkey(config["RadioButton"], callback=useRadio)
ahk.start_hotkeys()

# ctrl+c catch
signal.signal(signal.SIGINT, signal.SIG_DFL)

# run (may be we dont need it with no overlay)
app.exec()
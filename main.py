from recognizer import VoskRecognizer
from overlay import Overlay
from ahk import AHK
from PyQt5.QtWidgets import QApplication

import time, signal

import json

with open('config.json', 'r') as file:
    config = json.load(file)

# app overlay
app = QApplication([])
overlay = Overlay()

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
        overlay.listeningMode()
        speech = r.recognizeMic()
        if speech and len(speech) > 0:
            chat(speech)
        overlay.waitingMode()

ahk.add_hotkey(config["RadioButton"], callback=useRadio)
ahk.start_hotkeys()

# ctrl+c
signal.signal(signal.SIGINT, signal.SIG_DFL)

# run
app.exec()
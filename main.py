from recognizer import VoskRecognizer
from overlay import Overlay
from ahk import AHK
from PyQt5.QtWidgets import QApplication

import time, signal

app = QApplication([])
overlay = Overlay()

r = VoskRecognizer()
r.start()

try:
    ahk = AHK()
except:
    ahk = AHK(version="v2")

def chat(str):
    ahk.send("{^}")
    ahk.send("{Escape}")
    ahk.send("{t}")
    time.sleep(0.1)
    ahk.send_raw("{}".format(str))
    ahk.send("{Enter}")
    time.sleep(0.1)
    ahk.send("{Escape}")

def useRadio():
    if ahk.active_window.get_process_name() == "iRacingSim64DX11.exe":
        overlay.listeningMode()
        speech = r.recognizeMic()
        if speech and len(speech) > 0:
            chat(speech)
        overlay.waitingMode()

ahk.add_hotkey('0', callback=useRadio)
ahk.start_hotkeys()

signal.signal(signal.SIGINT, signal.SIG_DFL)

app.exec()
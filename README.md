# pySimRadio

A simple Text-to-Chat for iRacing racers using python.

# Third-Party python dependencies

This program uses several third-party dependencies that must be installed using pip or similar:

https://pypi.org/project/SpeechRecognition/ - it has a nice microphone audio reader.

https://pypi.org/project/PyQt5/ - for the overlay

https://pypi.org/project/vosk/ - for transcription

https://pypi.org/project/ahk/ - for controller/keyboard management

https://pypi.org/project/playsound3/ - for the "bip" sfx

# Third-Party non-python dependencies

## AutoHotkey

A valid AutoHotkey installation is required. The executable must be available through any of these options:

- PATH enviroment variable
- AHK_PATH enviroment variable
- "C:\Program Files\AutoHotkey" or "C:\Program Files\AutoHotkey\v2" directory

A valid path can also be established by modifying the code in main.py

> ahk = AHK(executable_path="Path/To/AutoHokey.exe")

or 

> ahk = AHK(version="v2", executable_path="Path/To/v2/AutoHokey.exe")

## vosk model

A vosk model must be downloaded in order to use this program. Many models are available at https://alphacephei.com/vosk/models.

Download the model for the language you want to use and decompress its contents into the program folder, then rename it to "model"

A custom path can also be established by modifying the code in main.py:

> r.start(model="Path/To/Model/Directory")
# pySimRadio

A VERY simple Speech-to-Chat for iRacing racers using python. Dont expect complex code or nice UIs.

# Settings

## "Radio" button

Edit config.json file and sets the RadioButton to one of these valid values: https://www.autohotkey.com/docs/v2/KeyList.htm

For Wheels/gamepad buttons only the first 32 coded buttons are available, from "Joy1" to "Joy32" for controller 1, "2Joy1" to "2Joy32" for controller 2 and so on till "16Joy1" to "16Joy32" (16 is the max number of controllers available for reading). If you want to use higher idexed buttons you will have to remap them using the program suplied by the manufacturer or any other, or even maping to the keyboard and using the maped key, to do it just use a program like Antimicrox (https://github.com/AntiMicroX/antimicrox).

To know the number of the device you want to use run:

> joy.cpl

Devices are sorteds in ordinal (or should it).

Note if you set a keyboard button it will block they original functionality. And if you edit json file you will need to re-run the program to apply the changes.

## No Overlay

Edit config.json file and sets the Overlay value to 0 to dont show the overlay.

## Auto hide after first radio call

Edit config.json file and sets the AutoHideIdle to 1 for hide the overlay after the first use, or sets 0 to keep it visible. Of course, it will not produce any effect if Overlay vale is set to 0.

# Running

> python main.py

# Third-Party python dependencies

This program uses several third-party dependencies that must be installed using pip or similar:

https://pypi.org/project/SpeechRecognition/ - it has a nice microphone audio reader.

https://pypi.org/project/PyQt5/ - for the overlay

https://pypi.org/project/vosk/ - for transcription

https://pypi.org/project/ahk/ - for controller/keyboard management

https://pypi.org/project/playsound3/ - for the "bip" sfx

All these ones are libs wich really deserve some credit of this program. All-in-one pip install:

> pip install SpeechRecognition vosk pyqt5 ahk playsound3

# Third-Party non-python dependencies

## AutoHotkey

A valid AutoHotkey installation is required. The executable must be available through any of these options:

- PATH enviroment variable
- AHK_PATH enviroment variable
- "C:\Program Files\AutoHotkey" or "C:\Program Files\AutoHotkey\v2" directory

A valid path can also be established by modifying the code in main.py

> ahk = AHK(executable_path="Path/To/AutoHotkey.exe")

or 

> ahk = AHK(version="v2", executable_path="Path/To/v2/AutoHotkey.exe")

## vosk model

A vosk model must be downloaded in order to use this program. Many models are available at https://alphacephei.com/vosk/models.

Download the model for the language you want to use and decompress its contents into the program folder, then rename it to "model"

A custom path can also be established by modifying the code in main.py:

> r.start(model="Path/To/Model/Directory")

# Turn off the radio

Right clicking the overlay and select this option or Ctrl+C on the terminal you use to run the program (or even closing that terminal).
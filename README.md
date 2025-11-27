# pySimRadio

A simple but useful app for iRacing racers using python and following KISS an reuse code principles. Dont expect a nice UIs.

The project was started as a Speech2Chat application, with the aim of transcribing what was dictated into the microphone into the iRacing chat. Although this feature is part of the application called FreeRadio, it should be noted that in some cases the transcription may be faulty and an unwanted message may end up being sent to the chat.

That is why an Engineer version has been included that only responds when the voice command matches a series of user-defined patterns. The Engineer can write messages for you in the chat, press keys, or dictate any information you request by voice.

This application is not intended to replace much more powerful applications such as CrewChief or DRE, but has simply been designed as an easily modifiable complement to them using a popular language such as Python.

However, it is not necessary to know this programming language, and for most users, it will only be necessary to be familiar with regular expressions to add functionality through the single configuration file called config.json.

The application can also use third-party online services, which are freely available to the community, to translate messages. So, for example, if, like the author, English is not your native language and you find it difficult to vocalize, you can use a transcriber in your native language and the message will be translated into the language you have designated.

# Third-Party python dependencies

> [!NOTE]
> First of all, at november'25, i recomend using python 3.13 to fit issues with pyAudio.

This program uses **several third-party dependencies** that must be installed using pip or similar:

> [!IMPORTANT]
> All these ones are libs wich really deserve some credit of this app. If you plan to use this application frequently buy his authors a coffee, make a donation, or so to everyone, if possible.

https://pypi.org/project/SpeechRecognition/ - it has a nice microphone audio reader.

https://pypi.org/project/PyQt5/ - for the overlay

https://pypi.org/project/vosk/ - for transcription

https://pypi.org/project/ahk/ - for controller/keyboard management

https://pypi.org/project/playsound3/ - for the "bip" sfx

https://pypi.org/project/num2words/ - self-explained

https://pypi.org/project/deep-translator/ - for translation

https://pypi.org/project/pyttsx3/ - Text to speech

All-in-one pip install:

> pip install SpeechRecognition vosk pyqt5 ahk playsound3 num2words deep-translator pyttsx3

## Troubleshoting with pyAudio

SpeechRecognition requires pyAudio module installed with is a bit a headpain issue. There is a precompiled version using the wheel wich can be installed via:

> pip install pyaudio

Using python 3.13 and the "pip install pyaudio" method is working well.

# Third-Party non-python dependencies

## AutoHotkey

A valid AutoHotkey installation is required. The executable must be available through any of these options:

- PATH enviroment variable
- AHK_PATH enviroment variable
- "C:\Program Files\AutoHotkey" or "C:\Program Files\AutoHotkey\v2" directory

A valid path can also be established in config.json by adding this key/value pair:

> "AhkPath": "Path/To/v2/AutoHotkey.exe"

Note that "Path/To/v2/AutoHotkey.exe" must be a real and valid path.

## vosk model

A vosk model must be downloaded in order to use this script. Many models are available at https://alphacephei.com/vosk/models.

Download the model for the language you want to use and decompress its contents into the main folder, then rename it to "model" witch is the default location. You can set a custom location modifying the "VoskModelPath" value in config.json.

> [!NOTE]
> "DriverLanguage" must match the language of the model.

# Other settings

## Free "Radio" button

Edit config.json file and sets the FreeRadioButton to one of these valid values: https://www.autohotkey.com/docs/v2/KeyList.htm

For Wheels/gamepad buttons only the first 32 coded buttons are available, from "Joy1" to "Joy32" for controller 1, "2Joy1" to "2Joy32" for controller 2 and so on till "16Joy1" to "16Joy32" (16 is the max number of controllers available for reading). If you want to use higher idexed buttons you will have to remap them using the application suplied by the manufacturer or any other, or even maping to the keyboard and using the maped key, to do it just use an application like Antimicrox (https://github.com/AntiMicroX/antimicrox).

To know the number of the device you want to use run:

> joy.cpl

Devices are sorteds in ordinal (or should it).

Note if you set a keyboard button it will block they original functionality. And if you edit json file you will need to re-run the script to apply the changes.

## Engineer Radio Button

The EngineerButton is used to send commands to your engineer. He will only understand certain commands and ignore what it does not understand. Your engineer can type for you in the chat and also press keys for you.

## No Overlay

Edit config.json file and sets the Overlay value to 0 to dont show the overlay.

## Auto hide after first radio call

Edit config.json file and sets the AutoHideIdle to 1 for hide the overlay after the first use, or sets 0 to keep it visible. Of course, it will not produce any effect if Overlay vale is set to 0.

# Running

> python main.py

# Stop running

Right clicking the overlay and select this option or Ctrl+C on the terminal you use to run the script (or even closing that terminal).

# Commands

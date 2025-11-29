# pySimRadio

A simple but useful app for iRacing racers using python and following KISS an reuse code principles. Dont expect a nice UIs.

The project was started as a Speech2Chat application, with the aim of transcribing what was dictated into the microphone into the iRacing chat. Although this feature is part of the application called FreeRadio, it should be noted that in some cases the transcription may be faulty and an unwanted message may end up being sent to the chat.

That is why an Engineer version has been included that only responds when the voice command matches a series of user-defined patterns. The Engineer can write messages for you in the chat, press keys, or dictate any information you request by voice.

This application is not intended to replace much more powerful applications such as CrewChief or DRE, but has simply been designed as an easily modifiable complement to them using a popular language such as Python.

However, it is not necessary to know this programming language, and for most users, it will only be necessary to be familiar with regular expressions to add functionality through the single configuration file called config.json.

The application can also use third-party online services, which are freely available to the community, to translate messages. So, for example, if, like the author, English is not your native language and you find it difficult to vocalize, you can use a transcriber in your native language and the message will be translated into the language you have designated.

If find it useful and you want to support, buy me a coffee:

<a href="https://www.buymeacoffee.com/arrecio"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-orange.png" height="40px"></a>


# Third-Party python dependencies

> [!NOTE]
> First of all, at november'25, i recomend using python 3.13 to fit issues with pyAudio.

This program uses **several third-party dependencies** that must be installed using pip or similar:

> [!IMPORTANT]
> All these ones are libs wich really deserve some credit of this app. If you plan to use this application frequently buy his authors a coffee, make a donation, or so to everyone, if possible.

- https://pypi.org/project/SpeechRecognition/ - it has a nice microphone audio reader.
- https://pypi.org/project/PyQt5/ - for the overlay
- https://pypi.org/project/vosk/ - for transcription
- https://pypi.org/project/ahk/ - for controller/keyboard management
- https://pypi.org/project/playsound3/ - for the "bip" sfx
- https://pypi.org/project/num2words/ - self-explained
- https://pypi.org/project/deep-translator/ - for translation
- https://pypi.org/project/pyttsx3/ - Text to speech

All-in-one pip install:

> pip install SpeechRecognition vosk pyqt5 ahk playsound3 num2words deep-translator pyttsx3

## Troubleshoting with pyAudio

SpeechRecognition requires pyAudio module installed with is a bit a headpain issue. There is a precompiled version using the wheel wich can be installed via:

> pip install pyaudio

Using python 3.13 and the "pip install pyaudio" method is working well. Para instalar esta versión con winget:

> winget install -e --id Python.Python.3.13

También puedes utilizar la Microsoft Store o cualquier otro método que conozcas.

# Third-Party non-python dependencies

## AutoHotkey

A valid AutoHotkey installation is required. The executable must be available through any of these options:

- PATH enviroment variable
- AHK_PATH enviroment variable

- "C:\Program Files\AutoHotkey" or "C:\Program Files\AutoHotkey\v2" directory

A valid path can also be established in config.json by adding this key/value pair:

> "AhkPath": "Path/To/v2/AutoHotkey.exe"

Note that "Path/To/v2/AutoHotkey.exe" must be a valid path in your system.

## vosk model

A vosk model must be downloaded in order to use this script. Many models are available at https://alphacephei.com/vosk/models.

Download the model for the language you want to use and decompress its contents into the main folder, then rename it to "model" witch is the default location. You can set a custom location modifying the "VoskModelPath" value in config.json.

> [!NOTE]
> "DriverLanguage" must match the language of the model for a correct trascription.

# Other settings

## Free "Radio" button

Edit config.json file and sets the FreeRadioButton to one of these valid values: https://www.autohotkey.com/docs/v2/KeyList.htm

For Wheels/gamepad buttons only the first 32 coded buttons are available, from "Joy1" to "Joy32" for controller 1, "2Joy1" to "2Joy32" for controller 2 and so on till "16Joy1" to "16Joy32" (16 is the max number of controllers available for reading). If you want to use higher idexed buttons you will have to remap them using the application suplied by the manufacturer or any other, or even maping to the keyboard and using the maped key, to do it just use an application like Antimicrox (https://github.com/AntiMicroX/antimicrox).

To know the number of the device you want to use run:

> joy.cpl

Devices are sorteds in ordinal (or should it). In adition, pressing the properties button you can easy find the button number by pressing the one you want to use.  

Note if you set a keyboard button it will block they original functionality. And if you edit json file you will need to re-run the script to apply the changes.

## Engineer Calling Button

The EngineerButton is used to send commands to your engineer. He will only understand certain commands and ignore what it does not understand. Your engineer can type for you in the chat and also press keys for you.

## No Overlay

Edit config.json file and sets the Overlay value to 0 to dont show the overlay.

## Auto hide after first radio call

Edit config.json file and sets the AutoHideIdle to 1 for hide the overlay after the first use, or sets 0 to keep it visible. Of course, it will not produce any effect if Overlay vale is set to 0.

# Running

> python main.py

# Stop running

Right clicking the overlay and select this option or Ctrl+C on the terminal you use to run the script (or even closing that terminal).

# Working with Engineer commands

Commands must be set in the EngineerCommands branch of the config.json file. 

They must contain a structure with two main keys:

- “command”: must contain the text that activates the command. It can be a regular expression.

- “type”: indicates the type of command. There are currently four types: “chat” to write in the chat, “say” to vocalize a response, ‘keypress’ to press a key or combination of keys, and “run” to execute a program.

Other keys will be as follows:

- “msg”: This will only be useful for the ‘chat’ and “say” command types, and will be the message to send or listen to. This message can contain escape characters to replace groups captured in the command and also variables to be replaced using data captured from the game. For example, “{p1time}” will be replaced by the time at position 1.

- “path”: path to the program to be executed in the case of the “run” command type

- “keys”: keys to press in the case of the “keypress” command. See: https://www.autohotkey.com/docs/v2/lib/Send.htm

## Things to keep in mind

Transcribed messages undergo some transformations before being analyzed as regular expressions. These should be taken into account:

- The expression “position” followed by a number, such as 8, which would be “position 8,” is considered P8.

- The expression “leader” is expressed as P1.

In the regular expression, we can define different capture groups (see https://www.w3schools.com/python/python_regex.asp).

An example of a command to request the last lap of the position 1:

>{
>"command": "^P1 time",
>"type": "say",
>"msg": "{p1lasttime}"
>},

But you can build a command for get this info for any other position using regex:

>{
>"command": "^P(\\d*) time",
>"type": "say",
>"msg": "{p\\1lasttime}"
>},

> [!NOTE]
> The backslash must be double backslashes in text editors.

## Usage of the real-time game data

{p1lasttime} is an expression to be replaced in the final message. These types of expressions are enclosed in curly brackets. They can be any of the following, where # represents a number between 0 and 999.

- {timestamp} - Current time.
- {p#lasttime} - Last lap time for position #.
- {p#besttime} - Best lap time for position #.
- {p#name} - Name of the driver in position #.
- {playerposition} - The player's race position.

This is a basic list that has been implemented with the sole intention of testing functionality. More will be added in the future.

## Auto commands for translating messages

In the EngineerTranslations branch, the key/value pairs will create commands to translate messages using GoogleTranslator. The pairs must follow this pattern:

“language”: “language code”

“language” will be the first word of the command, so it does not necessarily have to be the name of the language, although that would be the most obvious choice.

For example, we could configure the translations as follows:

> “EngineerTranslations”: {
> “coffee”: “es”
> }

With this, if we send a command to the engineer that says “coffee today is a nice day,” it will send “Hoy es un buen día” to the chat becouse "es" mean spanish. See https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes for all codes. Note that may be not everyone are supporteds.

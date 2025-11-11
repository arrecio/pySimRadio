
import speech_recognition as sr
import json
from vosk import KaldiRecognizer, Model, SetLogLevel
from playsound3 import playsound
import os

class VoskRecognizer:
    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__microphone = sr.Microphone()
        self.__rec = None
        self.__busy = False

    # loads the vosk model
    def start(self, model="model"):
        if not self.__rec:
            if not os.path.exists(model):
                print("Please download the model from https://alphacephei.com/vosk/models and un9pack as 'model' in the current folder to use this as default or set the 'model' argument with their path to VoskRecognizer.start(model='model_path').")
                exit()
            self.__vosk_model = Model(model)
            self.__rec = KaldiRecognizer(self.__vosk_model, 16000)

    def isReady(self):
        return not self.__rec is None

    def recognizeMic(self):
        if not self.__rec:
            print("Recognizer not initialized. Please call start(model?) first.")
            return None
        if not self.__busy:
            playsound("media/radio.mp3", block = False)
            self.__busy = True
        else:
            return None

        with self.__microphone as source:
            # recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.__recognizer.listen(source, timeout=3)
            except:
                self.__busy = False
                return None

        self.__rec.AcceptWaveform(audio.get_raw_data(convert_rate=16000, convert_width=2))
        finalRecognition = self.__rec.FinalResult()
        response = json.loads(finalRecognition)
        recognition = response["text"] if response else finalRecognition
        self.__busy = False
        return recognition

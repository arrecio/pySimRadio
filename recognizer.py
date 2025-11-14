
import speech_recognition as sr
import os
import json
from vosk import KaldiRecognizer, Model
from playsound3 import playsound

class VoskRecognizer:
    def __init__(self, model="model"):
        self.__recognizer = sr.Recognizer()
        self.__microphone = sr.Microphone()
        self.__busy = False
        if not os.path.exists(model):
            print("Vosk model data not found. (see README.md)")
            exit()
        try:
            self.__vosk_model = Model(model)
            self.__rec = KaldiRecognizer(self.__vosk_model, 16000)
        except:
            print("Invalid Vosk model at '{}'. (see README.md)".format(model))
            exit()

    def isReady(self):
        return not self.__rec is None

    def recognizeMic(self):
        if not self.__busy:
            playsound("media/radio.mp3", block = False)
            self.__busy = True
        else:
            return None

        with self.__microphone as source:
            # self.__recognizer.adjust_for_ambient_noise(source)
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

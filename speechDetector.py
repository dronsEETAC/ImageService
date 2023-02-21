import speech_recognition as sr
import cv2


class SpeechDetector:
    def __init__(self):
        self.r = sr.Recognizer()

    def detect(self, level):
        with sr.Microphone() as source:
            print("habla")
            audio = self.r.listen(source, phrase_time_limit=1)
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                voice = self.r.recognize_google(audio, language="es-ES")
            except sr.UnknownValueError:
                voice = "?????"
            voice = voice.capitalize()
            print("has dicho ", voice)
        code = -1
        if level == "easy":
            if voice == "Norte":
                code = 1
            elif voice == "Sur":
                code = 2
            elif voice == "Este":
                code = 3
            elif voice == "Oeste":
                code = 4
            elif voice == "Drop":
                code = 5
            elif voice == "Retorna":
                code = 6
            elif voice == "Para":
                code = 0
        else:
            if voice == "Gazpacho":
                code = 1
            elif voice == "Luna":
                code = 2
            elif voice == "Platano":
                code = 3
            elif voice == "Amigo":
                code = 4
            elif voice == "Vamos":
                code = 5
            elif voice == "Casa":
                code = 6
            elif voice == "Castillo":
                code = 0

        return code, voice

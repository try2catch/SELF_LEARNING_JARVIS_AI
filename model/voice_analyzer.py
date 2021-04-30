import speech_recognition as sr
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class VoiceAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.recognizer = sr.Recognizer()

    def recognize(self):
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source=source, timeout=5, phrase_time_limit=5)
            voice_input = self.recognizer.recognize_google(audio)
            return self.sid.polarity_scores(voice_input)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print('Network error.')
        except sr.WaitTimeoutError:
            pass
        except TimeoutError:
            pass

import speech_recognition as sr
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import utils


class VoiceAnalyzer:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()

    def get_polarity_scores(self):
        try:
            voice_input = utils.read_voice_cmd()
            return self.sid.polarity_scores(voice_input)
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError:
            print('Network error.')
        except sr.WaitTimeoutError:
            pass
        except TimeoutError:
            pass

import os
import re

import speech_recognition as spr
from googletrans import Translator, constants
from gtts import gTTS

import utils


class Translate:
    INTENT_NAME = 'translate'

    def __init__(self, input, response):
        self.input = input
        self.response = response

    def get_text_and_target(self):
        text = utils.get_search_value(self.input, intent_name=Translate.INTENT_NAME, match_flag='sentence')
        last_char_index = re.search(r"\bin\b|\bto\b", text)
        if last_char_index:
            target = text[last_char_index.regs[0][1] + 1:]
            text = text[:last_char_index.regs[0][0] - 1]
            code = constants.LANGCODES.get(target)
            return text, code
        else:
            return None, None

    def translate(self):
        text, target = self.get_text_and_target()
        if target:
            try:
                translator = Translator(service_urls=['translate.googleapis.com'])
                text_to_translate = translator.translate(text, dest=target)
                text = text_to_translate.text

                speak = gTTS(text=text, lang=target, slow=False)
                speak.save("captured_voice.mp3")
                os.system("open captured_voice.mp3")
            except spr.UnknownValueError:
                print("Unable to Understand the Input")
            except spr.RequestError as e:
                print("Unable to provide Required Output".format(e))
        else:
            utils.speak('The asked language is not supported by me.')
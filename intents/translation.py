import os
import re
import time

import speech_recognition as sr
from googletrans import Translator, constants
from gtts import gTTS
from playsound import playsound

import config
import utils


class Translation:
    INTENT_NAME = 'translate'
    MP3_NAME = 'output.mp3'

    def __init__(self, input):
        self.input = input

    "how to speak my name is Akhilesh in Hindi"

    def get_text_and_target(self):
        text = utils.get_search_value(self.input, intent_name=Translation.INTENT_NAME, match_flag='sentence')
        last_char_index = re.search(r'\bin\b|\bto\b', text)
        if last_char_index:
            target = text[last_char_index.regs[0][1] + 1:]
            text = text[:last_char_index.regs[0][0] - 1]
            code = constants.LANGCODES.get(target)
        return text, code

    def translate(self):
        text, target = self.get_text_and_target()

        if target:
            try:
                translator = Translator(service_urls=['translate.googleapis.com'])
                text_to_translate = translator.translate(text, dest=target)
                text = text_to_translate.text

                speak = gTTS(text=text, lang=target, slow=False)
                speak.save(Translation.MP3_NAME)

                try:
                    if config.OS_NAME == 'Darwin':
                        os.system(f'open {Translation.MP3_NAME}')
                        time.sleep(5)
                    else:
                        playsound(Translation.MP3_NAME)
                    os.remove(Translation.MP3_NAME)
                except IOError:
                    pass
            except (sr.RequestError, sr.UnknownValueError) as e:
                print(e)
        else:
            utils.speak('The asked language is not supported by me.')

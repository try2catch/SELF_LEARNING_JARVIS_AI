import os
import random
import webbrowser

import pyttsx3

import config

engine = pyttsx3.init()


# def normalize_utterances(utterances):
#     normalized = ''
#     for u in utterances:
#         u = re.sub('\\W+', ' ', u)
#         normalized += u.lower().strip() + "|"
#
#     return normalized[:-1]


# def match_pattern(voice_note, pattern):
#     data = Utils.normalize_utterances(pattern)
#     compiled = re.compile(data)
#     value = compiled.search(voice_note)
#     if value:
#         return True
#     else:
#         False


def choose_random(response):
    return random.choice(response)


def play_sound(response):
    os_name = config.DEFAULT_OS_NAME
    if os_name == 'Darwin':
        os.system('say "{}"'.format(response))
    else:
        engine.say(response)
        engine.runAndWait()


def open(url):
    webbrowser.open(url)
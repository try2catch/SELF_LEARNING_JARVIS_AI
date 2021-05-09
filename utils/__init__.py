import os
import random
import webbrowser
import fnmatch
import pyttsx3
import re
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


def speak(response):
    os_name = config.DEFAULT_OS_NAME
    if os_name == 'Darwin':
        os.system('say "{}"'.format(response))
    else:
        engine.say(response)
        engine.runAndWait()


def open(url):
    webbrowser.open(url)


def find_file(pattern, path):
    paths = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                paths.append(os.path.join(root, name))

        if paths:
            return paths


def get_search_value(command, intent_name):
    intents = config.DATA['intents']
    utterances = [intent['utterances'] for intent in intents if intent['tag'] == intent_name][0]
    words = ['\\b' + word + '\\b' for utterance in utterances for word in utterance.split(' ')]
    words = '|'.join(words)
    return re.sub(words, '', command, flags=re.IGNORECASE).strip()

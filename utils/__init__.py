import fnmatch
import json
import os
import random
import re
import webbrowser

import pyttsx3

import config
from model.voice_analyzer import VoiceAnalyzer


def choose_random(response):
    return random.choice(response)


def speak(response):
    os_name = config.DEFAULT_OS_NAME
    if os_name == 'Darwin':
        os.system('say "{}"'.format(response))
    else:
        engine = pyttsx3.init()
        engine.say(response)
        engine.runAndWait()


def open_url(url):
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


def get_path_from_file(app):
    with open(config.APP_DETAILS_FILE) as file:
        app_details = json.load(file)

    app = app_details.get(app)
    if app:
        return app.get('path')


def get_path(app, ext, directories):
    patterns = [f'{app}*{ext}', f'{app}*.{ext}', f'*{app}.{ext}', f'*{app}*.{ext}']
    for directory in directories:
        for pattern in patterns:
            result = find_file(pattern, directory)
            if len(result):
                return get_multiple_paths(result)
            else:
                return result


def get_multiple_paths(paths, ext):
    speak('I got multiple applications. Which one would you like to open?')
    for path in paths:
        exe_name = os.path.basename(path).replace(ext, '')
        speak(exe_name)
        sentiments = VoiceAnalyzer().recognize()
        if sentiments:
            max_key = max(sentiments, key=sentiments.get)
            if max_key == 'neu' or max_key == 'pos':
                return path


def add_to_json(app_details):
    with open(config.APP_DETAILS_FILE, 'r+') as file:
        data = json.load(file)
        data.update(app_details)
        file.seek(0)
        json.dump(data, file)

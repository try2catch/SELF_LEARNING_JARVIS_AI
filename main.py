import os

import pyttsx3
import speech_recognition as sr

import config
import model
import utils
from intents.application import Applications
from model.model_training import TrainingModel


def read_voice_cmd(recognizer):
    voice_input = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            audio = recognizer.listen(source=source, timeout=5, phrase_time_limit=5)
        voice_input = recognizer.recognize_google(audio)
        print('Input : {}'.format(voice_input))
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print('Network error.')
    except sr.WaitTimeoutError:
        pass
    except TimeoutError:
        pass

    return voice_input.lower()


def play_sound(response, os_name, engine=None):
    if os_name == 'Darwin':
        # This will execute for mac ios.
        os.system(f'say "{response}"')
    else:
        engine.say(response)
        engine.runAndWait()


if __name__ == '__main__':
    words = model.words
    classes = model.classes

    training_model = TrainingModel(words, classes, model.data_x, model.data_y)
    trained_model = training_model.train()

    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    os = config.DEFAULT_OS_NAME
    session = False
    while True:
        command = read_voice_cmd(recognizer)
        if command or command is not '':
            intent = training_model.get_intent(trained_model, command)
            response = TrainingModel.get_response(intent, model.data)
            print(intent, ' : ', response)

            if intent == 'greeting':
                utils.play_sound(response=response, os_name=os)
                session = True
            elif session and intent == 'applications':
                Applications(response, os).launch(command)
                session = False

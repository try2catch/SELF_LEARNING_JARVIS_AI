import os
import platform

import pyttsx3
import speech_recognition as sr

import model
from model.model_training import TrainingModel


def read_voice_cmd(speech):
    voice_input = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            audio = speech.listen(source=source, timeout=5, phrase_time_limit=5)
        voice_input = speech.recognize_google(audio)
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


def playsound(response, os_name):
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

    speech = sr.Recognizer()
    engine = pyttsx3.init()
    os_name = platform.uname().system

    while True:
        command = read_voice_cmd(speech)
        intents = training_model.get_intent(trained_model, command)
        print('Intent : ', intents)
        response = TrainingModel.get_response(intents, model.data)
        playsound(response, os_name)

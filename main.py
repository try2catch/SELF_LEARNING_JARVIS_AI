import speech_recognition as sr

import config
import model
import utils
from intents.applications import Applications
from intents.youtube_search import YoutubeSearch
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


if __name__ == '__main__':
    words = model.words
    classes = model.classes

    training_model = TrainingModel(words, classes, model.data_x, model.data_y)
    trained_model = training_model.train()

    recognizer = sr.Recognizer()
    os = config.DEFAULT_OS_NAME
    session = True
    while True:
        command = read_voice_cmd(recognizer)
        if command or command is not '':
            intent = training_model.get_intent(trained_model, command)
            response = TrainingModel.get_response(intent, config.DATA)
            print(intent, ' : ', response)

            if intent == 'greeting':
                utils.speak(response=response)
                session = True
            elif session and intent == 'applications':
                Applications(response).launch(command)
                # session = False
            elif session and intent == 'youtube_search':
                YoutubeSearch(command, response).launch()
                session = False

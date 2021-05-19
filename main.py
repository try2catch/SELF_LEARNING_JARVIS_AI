import config
import model
import utils
from intents.alarm import Alarm
from intents.applications import Applications
from intents.youtube_search import YoutubeSearch
from model.model_training import TrainingModel

if __name__ == '__main__':
    words = model.words
    classes = model.classes

    training_model = TrainingModel(words, classes, model.data_x, model.data_y)
    trained_model = training_model.train()

    os = config.DEFAULT_OS_NAME
    session = False
    while True:
        command = utils.read_voice_cmd()
        if command or command is not '':
            intent = training_model.get_intent(trained_model, command)
            response = TrainingModel.get_response(intent, config.DATA)
            print(intent, ' : ', response)

            if intent == 'greeting':
                utils.speak(response=response)
                session = True
                continue
            elif session and intent == 'applications':
                Applications(response).launch(command)
                session = False
                continue
            elif session and intent == 'youtube_search':
                YoutubeSearch(command, response).launch()
                session = False
                continue
            elif intent == 'alarm':
                Alarm(command, response).start()
                continue

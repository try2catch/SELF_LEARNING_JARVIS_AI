import os.path
import json
import config
import utils
from model.voice_analyzer import VoiceAnalyzer


class WinApplications:
    APP_INSTALLATION_DIRECTORIES = ['C:\\Program Files', 'C:\\Program Files (x86)', 'C:\\Windows\\System32']

    def __init__(self, app):
        self.app = app

    def get_path(self):
        patterns = [f'{self.app}.exe', f'{self.app}*.exe', f'*{self.app}.exe', f'*{self.app}*.exe']
        for pattern in patterns:
            for directory in self.APP_INSTALLATION_DIRECTORIES:
                result = utils.find_file(pattern, directory)
                if result:
                    return result

    @staticmethod
    def get_multiple_paths(paths):
        utils.speak('I got multiple applications. Which one would you like to open?')
        for path in paths:
            exe_name = os.path.basename(path).replace('.exe', '')
            utils.speak(exe_name)
            sentiments = VoiceAnalyzer().recognize()
            if sentiments:
                max_key = max(sentiments, key=sentiments.get)
                if max_key == 'neu' or max_key == 'pos':
                    return path

    def get_path_from_file(self):
        with open(config.APP_DETAILS_FILE) as file:
            app_details = json.load(file)

        app = app_details.get(self.app)
        if app:
            return app.get('path')

    @staticmethod
    def add_to_json(app_details):
        with open(config.APP_DETAILS_FILE, 'r+') as file:
            data = json.load(file)
            data.update(app_details)
            file.seek(0)
            json.dump(data, file)

import re
import subprocess

import config
import utils

from intents.windows.win_applications import WinApplications


class Applications:
    INTENT_NAME = 'applications'

    def __init__(self, response, logger=None):
        self.logger = logger
        self.response = response
        self.os_name = config.DEFAULT_OS_NAME

    def get_name(self, command):
        app = utils.get_search_value(command, intent_name=self.INTENT_NAME)

        is_space = bool(re.search(r"\s", app))
        if is_space:
            return app.replace(' ', "\\ ")
        else:
            return app

    def launch(self, command):
        app = self.get_name(command)
        if self.os_name == 'Darwin':
            cmd = f"open /Applications/{app}.app"
            self.execute_command(cmd)
        else:
            winapp = WinApplications(app)

            path = winapp.get_path_from_file()
            if path is None:
                paths = winapp.get_path()
                if len(paths) > 1:
                    path = WinApplications.get_multiple_paths(paths)
                else:
                    path = paths[0]
                WinApplications.add_to_json({app: {'path': path}})
            if path:
                cmd = f'explorer "{path}"'
                print('Application : ', cmd)
                self.execute_command(cmd)

    def execute_command(self, cmd):
        utils.speak(response=self.response)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if str(output[1], 'utf-8') is not '':
            utils.speak('I am sorry sir, The app which you are looking for is not installed in my database.')

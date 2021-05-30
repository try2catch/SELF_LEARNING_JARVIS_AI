import os
import re
import subprocess

import config
import utils
from intents import windows


class Applications:
    INTENT_NAME = 'applications'
    APP_INSTALLATION_DIRECTORIES = ['/System/Applications', '/Applications', '/System/Applications/Utilities']

    def __init__(self, response, logger=None):
        self.logger = logger
        self.response = response
        self.os_name = config.OS_NAME

    def get_name(self, command):
        app = utils.get_search_value(command, intent_name=Applications.INTENT_NAME)

        is_space = bool(re.search(r"\s", app))
        if is_space:
            return app.replace(' ', "\\ ")
        else:
            return app

    def launch(self, command):
        app = self.get_name(command)

        if self.os_name == 'Darwin':
            path = utils.get_path_from_file(app)
            if path is None:
                patterns = [f'*{app}.app', f'{app}*.app', f'*{app}.app', f'*{app}*.app']
                for directory in Applications.APP_INSTALLATION_DIRECTORIES:
                    if path:
                        break
                    for pattern in patterns:
                        path = os.popen(f"find {directory} -iname '{pattern}'").read() \
                            .split('\n')[0].replace(" ", "\\ ")
                        if path:
                            break

            cmd = f'open {path}'
            self.execute_command(cmd)
            utils.add_to_json({app: {'path': path}})
        else:
            path = utils.get_path_from_file(app)
            if path is None:
                path = utils.get_path(app, windows.EXECUTABLE_EXT, windows.APP_INSTALLATION_DIRECTORIES)
                utils.add_to_json({app: {'path': path}})
            if path:
                cmd = f'explorer "{path}"'
                print('Application : ', cmd)
                self.execute_command(cmd)

    def execute_command(self, cmd):
        utils.speak(response=self.response)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if str(output[1], 'utf-8') is not '':
            utils.speak('I am sorry sir, The app which you are looking for is not installed in my database.')

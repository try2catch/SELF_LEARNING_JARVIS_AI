import re
import subprocess

import utils


class Applications:
    def __init__(self, response, os_name, logger=None):
        self.logger = logger
        self.response = response
        self.os_name = os_name

    @staticmethod
    def get_name(command):
        app = command.split(' ', 1)[1]

        is_space = bool(re.search(r"\s", app))
        if is_space:
            return app.replace(' ', "\\ ")
        else:
            return app

    def launch(self, command):
        app = Applications.get_name(command)
        cmd = f"open /Applications/{app}.app"
        print('Application : ', cmd)
        output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if str(output[1], 'utf-8') is not '':
            utils.play_sound('I am sorry sir, The app which you are looking for is not installed in my database.',
                             os_name=self.os_name)
        else:
            utils.play_sound(response=self.response, os_name=self.os_name)

import re

import dateparser

from utils import alarm_utils


class AlarmTiming:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def match(string, regex):
        compiled = re.compile(regex, flags=re.IGNORECASE)
        result = compiled.search(string)
        if result:
            return result.group()
        else:
            return ''

    def get_expected_time(self):

        date_time_str = ''
        # Minutes
        # time = AlarmTiming.match(self.text, alarm_utils.minutes_regex)
        # date_time_str += time

        day = AlarmTiming.match(self.text, alarm_utils.days_regex)
        date_time_str += day

        hours = AlarmTiming.match(self.text, alarm_utils.hours_regex)
        date_time_str += hours

        # AM PM
        day_night = AlarmTiming.match(self.text, alarm_utils.day_night_regex)
        date_time_str += day_night

        period = AlarmTiming.match(self.text, alarm_utils.period_regex)
        date_time_str += period
        print('Timing String from regex :' + date_time_str)

        value = dateparser.parse(date_time_str)
        print('Parsed text to datetime :' + str(value))

        if value:
            return value.strftime('%Y-%m-%d %H:%M:00')

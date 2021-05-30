import dateparser

import utils
from utils import alarm_utils


class AlarmTiming:
    def __init__(self, text):
        self.text = text

    def get_expected_time(self):
        date_time_str = ''
        # Minutes
        # time = AlarmTiming.match(self.text, alarm_utils.minutes_regex)
        # date_time_str += time

        day = utils.match(self.text, alarm_utils.days_regex)
        date_time_str += day

        hours = utils.match(self.text, alarm_utils.hours_regex)
        date_time_str += hours

        # AM PM
        day_night = utils.match(self.text, alarm_utils.day_night_regex)
        date_time_str += day_night

        period = utils.match(self.text, alarm_utils.period_regex)
        date_time_str += period
        print('Timing String from regex :' + date_time_str)

        value = dateparser.parse(date_time_str)
        print('Parsed text to datetime :' + str(value))

        if value:
            return value.strftime('%Y-%m-%d %H:%M:00')

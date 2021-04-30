import html
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config
import utils
from model.voice_analyzer import VoiceAnalyzer


class YoutubeSearch:
    DEVELOPER_KEY = "<REPLACE THIS WITH YOUR KEY>"
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_VERSION = 'v3'

    def __init__(self, command, response):
        self.command = command
        self.response = response
        self.os = config.DEFAULT_OS_NAME

    def get_search_value(self):
        'search friday in python on youtube'
        intents = config.DATA['intents']
        utterances = [intent['utterances'] for intent in intents if intent['tag'] == 'youtube_search'][0]
        words = set(['\\b' + word + '\\b' for utterance in utterances for word in utterance.split(' ')])
        words = '|'.join(words)
        return re.sub(words, '', self.command, flags=re.IGNORECASE).strip()

    def search(self):
        try:
            youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_VERSION, developerKey=self.DEVELOPER_KEY)

            search = self.get_search_value()
            search_response = youtube.search().list(
                q=search,
                part='id, snippet',
                maxResults=1
            ).execute()

            return search_response.get('items')
        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occured: {e.content}')

    def open(self, url):
        sentiments = VoiceAnalyzer().recognize()
        if sentiments:
            max_key = max(sentiments, key=sentiments.get)
            if max_key == 'neu' or max_key == 'pos':
                utils.open(url)
                utils.play_sound(self.response)

    def launch(self):
        result = self.search()[0]
        title = html.unescape(result['snippet']['title'])

        if result['id']['kind'] == 'youtube#video':
            utils.play_sound(f'I have found the video as {title}. Would you like to play it?')
            url = f"https://youtu.be/{result['id']['videoId']}"
        elif result['id']['kind'] == 'youtube#channel':
            utils.play_sound(f'I got a channel for you as {title}. Would you like to open it?')
            url = f"https://www.youtube.com/channel/{result['id']['channelId']}"

        self.open(url)

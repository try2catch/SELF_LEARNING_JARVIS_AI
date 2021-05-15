import html

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config
import utils
from model.voice_analyzer import VoiceAnalyzer


class YoutubeSearch:
    DEVELOPER_KEY = "<REPLACE THIS WITH YOUR KEY>"
    INTENT_NAME = 'youtube_search'

    def __init__(self, command, response):
        self.command = command
        self.response = response
        self.os = config.DEFAULT_OS_NAME

    def search(self):
        try:
            youtube = build('youtube', 'v3', developerKey=YoutubeSearch.DEVELOPER_KEY)

            search = utils.get_search_value(self.command, YoutubeSearch.INTENT_NAME)
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
                utils.speak(self.response)
                utils.open_url(url)

    def launch(self):
        try:
            result = self.search()[0]

            title = html.unescape(result['snippet']['title'])

            if result['id']['kind'] == 'youtube#video':
                utils.speak(f'I have found the video as {title}. Would you like to play it?')
                url = f"https://youtu.be/{result['id']['videoId']}"
            elif result['id']['kind'] == 'youtube#channel':
                utils.speak(f'I got a channel for you as {title}. Would you like to open it?')
                url = f"https://www.youtube.com/channel/{result['id']['channelId']}"

            self.open(url)

        except HttpError as e:
            print(e)

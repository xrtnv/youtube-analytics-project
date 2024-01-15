import json
import os
import re

from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        if not re.match(r"^[a-zA-Z0-9_-]{24}$", channel_id):
            raise ValueError("Invalid YouTube channel ID")
        self._channel_id = channel_id

    def fetch_info(self) -> None:
        """Получает информацию о канале через API."""
        try:
            api_key = str('AIzaSyDJ7nw2WYTf8aOKlpLQ7laJn6vYDyLbh_M')
            # api_key = str(os.getenv('YOUTUBE_API_KEY'))
            # Не получает ничего, хотя по другим переменным вытягивает, поэтому применил
            # то, что выше
            youtube = build('youtube', 'v3', developerKey=api_key)
            channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
            print(channel)
        except Exception as e:
            pass

    def get_info(self) -> str:
        """Возвращает информацию о канале в виде строки."""
        self.fetch_info()


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(self.get_info())

import json
from typing import Iterator, List
import re


class Cleaner:
    def __init__(self):
        with open('stopwords.json', 'rt') as file:
            self.stop_words: List[str] = json.loads(file.read())
        self.re_str_abbr = r"\b[0-9]*[-]*[A-ZА-Я]{1,}[a-zа-я]*[A-ZА-Я]{1,}[-]*[a-zA-Zа-яА-Я0-9]*\b"

    def remove_stop_words(self, words: Iterator[str]) -> List[str]:
        """
        Убирает стоп-слова из списка
        """
        return [word for word in words if word not in self.stop_words]

    def retrieve_abbrs(self, text: str) -> List[str]:
        """
        Находит аббревиатуры приложения
        :param text: предложение
        :return: список аббревиатур приложения
        """
        return re.findall(self.re_str_abbr, text)

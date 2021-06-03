import json
from typing import Iterator, List
import re


class Cleaner:
    def __init__(self):
        with open('stopwords.json', 'rt') as file:
            self.stop_words: List[str] = json.loads(file.read())

    def delete_stop_words(self, words: Iterator[str]) -> List[str]:
        """
        Убирает стоп-слова из списка
        """
        return [word for word in words if word not in self.stop_words]

    def get_letter_words(self, text: str) -> List[str]:
        """
        Производит токенизацию предложения
        :param text: предложение
        :return: список слов из предложения
        """
        rep = re.compile("[^a-zA-Zа-яА-я]")
        letter_words = rep.sub(" ", text).lower()
        return re.findall(r'\b[а-яa-z]{3,15}\b', letter_words)

import re
from typing import List


class Abbreviations:
    def __init__(self):
        self.re_str_abbr = r"\b[0-9]*[-]*[A-ZА-Я]{1,}[a-zа-я]*[A-ZА-Я]{1,}[-]*[a-zA-Zа-яА-Я0-9]*\b"

    def __call__(self, text: str) -> List[str]:
        """
        Находит аббревиатуры приложения
        :param text: предложение
        :return: список аббревиатур приложения
        """
        return re.findall(self.re_str_abbr, text)



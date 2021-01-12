import re


class Abbreviations(object):
    def __init__(self):
        self.re_str_abbr = r"\b[0-9]*[-]*[A-ZА-Я]{1,}[a-zа-я]*[A-ZА-Я]{1,}[-]*[a-zA-Zа-яА-Я0-9]*\b"

    def __call__(self, text):
        return re.findall(self.re_str_abbr, text)



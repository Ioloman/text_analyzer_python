import re
from typing import List
from razdel import sentenize
from navec import Navec
from slovnet import NER


class Tokenizer:
    def __init__(self):
        navec = Navec.load('models/navec_news_v1_1B_250K_300d_100q.tar')
        self.ner = NER.load('models/slovnet_ner_news_v1.tar')
        self.ner.navec(navec)

    @staticmethod
    def split_to_sentences(text: str) -> List[str]:
        """
        Разбивает текст на предложения
        """
        return [sentence.text for sentence in sentenize(text)]

    @staticmethod
    def split_to_tokens(text: str) -> List[str]:
        """
        Производит токенизацию предложения
        :param text: предложение
        :return: список слов из предложения
        """
        rep = re.compile("[^a-zA-Zа-яА-я]")
        letter_words = rep.sub(" ", text).lower()
        return re.findall(r'\b[а-яa-z]{3,15}\b', letter_words)

    def get_ner(self, sentence: str) -> List[str]:
        """
        Возвращает список именованных сущностей из предложения
        :param sentence: предложение
        :return: список именованных сущностей
        """
        # не знаю зачем это было, я закомментил и
        # на всякий оставлю, вдруг баг появится
        # if sentence == []:
        #     sentence.append("")

        markup = self.ner(sentence)
        return [sentence[span.start: span.stop] for span in markup.spans]


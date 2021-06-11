from typing import Iterator, List
import pymorphy2
from rutermextract import TermExtractor


class Normalizer:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.term_extractor = TermExtractor()

    def normalize_ner(self, words: Iterator[str]) -> List[str]:
        """
        Приводит русские слова в нормальную форму
        """
        return [self.morph.parse(word)[0].normal_form for word in words]

    def get_normalized_key_tokens(self, sentence: List[str]) -> List[str]:
        """
        Выделяет ключевые слова в предложении и сразу нормализует их,
        используя PyMorphy
        :param sentence: список слов
        :return: список ключевых нормализованных слов
        """
        sentence = ' '.join(sentence)
        return [token.normalized for token in self.term_extractor(sentence)]

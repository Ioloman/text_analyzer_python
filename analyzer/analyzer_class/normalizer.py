# import maru
from typing import Iterator, List

import pymorphy2


class Normalizer(object):
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        # self.analyzer = maru.get_analyzer(tagger='crf', lemmatizer='pymorphy')

    def normalize_ner(self, words: Iterator[str]) -> List[str]:
        """
        Приводит русские слова в нормальную форму
        """
        return [self.morph.parse(word)[0].normal_form for word in words]

    # def normalize_ner(self, words):
    #     return [word.lemma for word in self.analyzer.analyze(words)]
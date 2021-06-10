from typing import Tuple, List, Iterator
from analyzer.analyzer_class.singleton_meta import SingletonMeta
from analyzer.analyzer_class.text_preprocessing import TextPreprocessing
from analyzer.analyzer_class.tf_idf import TFIDF, compute_tfidf
from analyzer.analyzer_class.candidates import Candidates
from analyzer.analyzer_class.tokenizer import Tokenizer


class Thesaurus(metaclass=SingletonMeta):
    def __init__(self):
        tokenizer = Tokenizer()
        self.text_preprocessing = TextPreprocessing(tokenizer)
        self.candidates = Candidates(tokenizer)
        self.tf_idf = TFIDF()
        self.alpha = 15
        self.betta = 1.7

    def __call__(self, text: str) -> Tuple[List[str], Iterator[Tuple[str, float]]]:
        clean_sentences, ner, abbr = self.text_preprocessing(text)
        candidates = self.candidates(clean_sentences, ner, abbr)
        keys, values = compute_tfidf(candidates)
        n = self.get_n(len(keys))
        keys, values = self.get_thesaurus_range(keys, values, n)
        return keys, zip(keys, values)

    def get_n(self, number_of_all_words: int) -> int:
        return round(pow(number_of_all_words/self.alpha, 1/self.betta))

    @staticmethod
    def get_thesaurus_range(keys: List[str], values: List[float], n: int) -> Tuple[List[str], List[float]]:
        return keys[0:n], values[0:n]


from itertools import chain

from joblib import Parallel, delayed

from analyzer.analyzer_class.cleaner import Cleaner
from analyzer.analyzer_class.tokenizer import Tokenizer
from analyzer.analyzer_class.abbreviations import Abbreviations
from analyzer.analyzer_class.normalizer import Normalizer


def clean(text, bad_words):
    for word in bad_words:
        text = text.replace(word, '')
    return text


class TextPreprocessing(object):
    def __init__(self, tokenizer: Tokenizer):
        self.cleaner = Cleaner()
        self.tokenizer = tokenizer
        self.abbreviations = Abbreviations()
        self.normalizer = Normalizer()
        self.size = 100000

    def __call__(self, text):

        # Токенизация по предложениям
        sentences = self.tokenizer.get_sentance(text)
        # Очистка предложений от аббревиатур
        sentences_abbr = list(map(self.abbreviations, sentences))
        clean_sentences = list(map(clean, sentences, sentences_abbr))
        # Выделение и нормализация именованных сущностей
        sentences_ner = list(map(self.tokenizer.get_ner, clean_sentences))
        clean_sentences = map(clean, clean_sentences, sentences_ner)
        sentences_ner = list(map(self.normalizer.normalize_ner, sentences_ner))
        # Токенизация по словам и удаление стоп-слов
        clean_sentences = map(self.cleaner.get_letter_words, clean_sentences)
        clean_sentences = list(map(self.cleaner.delete_stop_words, clean_sentences))

        return clean_sentences, sentences_ner, sentences_abbr

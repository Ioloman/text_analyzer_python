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
    def __init__(self):
        self.cleaner = Cleaner()
        self.tokenizer = Tokenizer()
        self.abbreviations = Abbreviations()
        self.normalizer = Normalizer()
        self.size = 100000

    def __call__(self, text):
        text_batch = [text[i: i + self.size] for i in range(0, len(text), self.size)]
        # sentences = self.tokenizer.get_sentance(text)
        sentences_map = Parallel(n_jobs=-1, backend="threading")(map(delayed(self.tokenizer.get_sentance), text_batch))
        sentences = list(chain.from_iterable(sentences_map))
        sentences_abbr = list(map(self.abbreviations, sentences))
        clean_sentences = list(map(clean, sentences, sentences_abbr))
        sentences_ner = list(map(self.tokenizer.get_ner, clean_sentences))
        clean_sentences = list(map(clean, clean_sentences, sentences_ner))
        sentences_ner = list(map(self.normalizer.normalize_ner, sentences_ner))
        clean_sentences = list(map(self.cleaner.get_letter_words, clean_sentences))
        clean_sentences = list(map(self.cleaner.delete_stop_words, clean_sentences))

        return clean_sentences, sentences_ner, sentences_abbr

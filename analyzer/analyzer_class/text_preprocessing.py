from typing import Iterator, List
from analyzer.analyzer_class.cleaner import Cleaner
from analyzer.analyzer_class.tokenizer import Tokenizer
from analyzer.analyzer_class.normalizer import Normalizer


def clean(text: str, bad_words: Iterator[str]) -> str:
    """
    Очищает строку от слов
    :param text: строка
    :param bad_words: слова
    :return: строка без слов
    """
    for word in bad_words:
        text = text.replace(word, '')
    return text


class TextPreprocessing:
    def __init__(self):
        self.cleaner = Cleaner()
        self.tokenizer = Tokenizer()
        self.normalizer = Normalizer()

    def __call__(self, text: str) -> List[List[str]]:
        # Токенизация по предложениям
        sentences = self.tokenizer.split_to_sentences(text)
        # Очистка предложений от аббревиатур
        sentences_abbr = list(map(self.cleaner.retrieve_abbrs, sentences))
        clean_sentences = list(map(clean, sentences, sentences_abbr))
        # Выделение и нормализация именованных сущностей
        sentences_ner = list(map(self.tokenizer.get_ner, clean_sentences))
        clean_sentences = map(clean, clean_sentences, sentences_ner)
        sentences_ner = map(self.normalizer.normalize_ner, sentences_ner)
        # Токенизация по словам и удаление стоп-слов
        clean_sentences_tokenized = map(self.tokenizer.split_to_tokens, clean_sentences)
        clean_sentences_tokenized = map(self.cleaner.remove_stop_words, clean_sentences_tokenized)
        # Извлечение ключевых слов
        sentences_candidates = map(self.normalizer.get_normalized_key_tokens, clean_sentences_tokenized)
        # Возвращение аббревиатур и именованных сущностей
        sentences_candidates = map(lambda l1, l2: l1 + l2, sentences_candidates, sentences_abbr)
        sentences_candidates = list(map(lambda l1, l2: l1 + l2, sentences_candidates, sentences_ner))

        return sentences_candidates

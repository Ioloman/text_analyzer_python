from typing import List
from analyzer.analyzer_class.tokenizer import Tokenizer


def list_compilation(one_list: List[List[str]], two_list: List[List[str]]) -> List[List[str]]:
    return [one_list[i] + two_list[i] for i in range(len(one_list))]


class Candidates(object):
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def __call__(self, sentences: List[List[str]], ner: List[List[str]], abbr: List[List[str]]) -> List[List[str]]:
        # Извлечение ключевых слов
        sentences_candidates = list(map(self.tokenizer.get_tokens, sentences))
        # Возвращение аббревиатур и именованных сущностей
        sentences_candidates = list_compilation(sentences_candidates, abbr)
        sentences_candidates = list_compilation(sentences_candidates, ner)
        return sentences_candidates

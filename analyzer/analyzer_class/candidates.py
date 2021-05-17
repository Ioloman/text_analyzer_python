from analyzer.analyzer_class.tokenizer import Tokenizer


def list_compilation(one_list, two_list):
    return [one_list[i] + two_list[i] for i in range(len(one_list))]


class Candidates(object):
    def __init__(self):
        self.tokenizer = Tokenizer()

    def __call__(self, sentences, ner, abbr):
        # Извлечение ключевых слов
        sentences_candidates = list(map(self.tokenizer.get_tokens,sentences))
        # Возвращение аббревиатур и именованных сущностей
        sentences_candidates = list_compilation(sentences_candidates, abbr)
        sentences_candidates = list_compilation(sentences_candidates, ner)
        return sentences_candidates

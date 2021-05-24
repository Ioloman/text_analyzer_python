import maru


class Normalizer(object):
    def __init__(self):
        self.analyzer = maru.get_analyzer(tagger='crf', lemmatizer='pymorphy')

    def normalize_ner(self, words):
        return [word.lemma for word in self.analyzer.analyze(words)]
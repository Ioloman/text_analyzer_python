from analyzer.analyzer_class.text_preprocessing import TextPreprocessing
from analyzer.analyzer_class.tf_idf import TFIDF
from analyzer.analyzer_class.candidates import Candidates

class Thesaurus(object):
    def __init__(self):
        self.text_preprocessing = TextPreprocessing()
        self.candidates = Candidates()
        self.tf_idf = TFIDF()
        self.alpha = 80
        self.betta = 0.9

    def __call__(self, text):
        clean_sentences, ner, abbr = self.text_preprocessing(text)
        candidates = self.candidates(clean_sentences, ner, abbr)
        keys, values = self.tf_idf(candidates)
        n = self.get_n(len(keys))
        keys, values = self.get_thesaurus_range(keys,values, n)
        return keys, zip(keys, values)

    def get_n(self,number_of_all_words):
        return round(pow(number_of_all_words/self.alpha,1/self.betta))

    def get_thesaurus_range(self, keys, values, n):
        return keys[0:n], values[0:n]


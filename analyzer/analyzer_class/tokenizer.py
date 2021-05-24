from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    NamesExtractor,
    Doc)

from rutermextract import TermExtractor


class Tokenizer(object):
    def __init__(self):
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.doc = []
        self.term_extractor = TermExtractor()

    def init_doc(self, text):
        self.doc = Doc(text)
        self.doc.segment(self.segmenter)
        self.doc.tag_ner(self.ner_tagger)

    def get_sentance(self, text):
        doc = Doc(text)
        doc.segment(self.segmenter)
        return [sentence.text for sentence in doc.sents]

    def get_tokens(self, sentence):
        sentence = ' '.join(sentence)
        return [token.normalized for token in self.term_extractor(sentence)]

    def get_ner(self, sentence):
        if sentence == []:
            sentence.append("")
        doc = Doc(sentence)
        doc.segment(self.segmenter)
        doc.tag_ner(self.ner_tagger)
        return [span.text for span in doc.spans]

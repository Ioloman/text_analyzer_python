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
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)
        self.doc = []
        self.term_extractor = TermExtractor()

    def init_doc(self, text):
        self.doc = Doc(text)
        self.doc.segment(self.segmenter)
        self.doc.tag_ner(self.ner_tagger)

    def get_sentance(self, text):
        segmenter = Segmenter()
        emb = NewsEmbedding()
        ner_tagger = NewsNERTagger(emb)
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)
        return [sentence.text for sentence in doc.sents]

    def get_tokens(self, sentence):
        sentence = ' '.join(sentence)
        return [token.normalized for token in self.term_extractor(sentence)]


    def get_ner(self, sentence):
        if sentence == []:
            sentence.append("")
        self.init_doc(sentence)
        return [span.text for span in self.doc.spans]

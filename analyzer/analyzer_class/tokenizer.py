from rutermextract import TermExtractor
from razdel import sentenize
from navec import Navec
from slovnet import NER


class Tokenizer(object):
    def __init__(self):
        self.term_extractor = TermExtractor()
        navec = Navec.load('models/navec_news_v1_1B_250K_300d_100q.tar')
        self.ner = NER.load('models/slovnet_ner_news_v1.tar')
        self.ner.navec(navec)

    def get_sentance(self, text):
        return [sentence.text for sentence in sentenize(text)]

    def get_tokens(self, sentence):
        sentence = ' '.join(sentence)
        return [token.normalized for token in self.term_extractor(sentence)]

    def get_ner(self, sentence):
        # не знаю зачем это было, я закомментил и
        # на всякий оставлю, вдруг баг появится
        # if sentence == []:
        #     sentence.append("")

        markup = self.ner(sentence)
        return [sentence[span.start: span.stop] for span in markup.spans]


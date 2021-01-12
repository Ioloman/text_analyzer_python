from nltk.corpus import stopwords
import re


class Cleaner(object):
    def __init__(self):
        self.stop_words = stopwords.words('russian')

    def delete_stop_words(self, words):
        return [word for word in words if word not in self.stop_words]

    def get_letter_words(self, text):
        rep = re.compile("[^a-zA-Zа-яА-я]")
        letter_words = rep.sub(" ", text).lower()
        return re.findall(r'\b[а-яa-z]{3,15}\b', letter_words)

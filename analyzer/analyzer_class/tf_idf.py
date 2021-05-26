from collections import Counter
from typing import List, Tuple, Dict
from gensim import corpora, models


class TFIDF:
    def __call__(self, texts: List[List[str]]) -> Tuple[List[str], List[float]]:
        """
        Определяет тезаурус и значения TF-IDF
        """
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        tf_idf = models.TfidfModel(corpus)
        corpus_tf_idf = tf_idf[corpus]
        tf_idf_saliency = Counter()
        for doc in corpus_tf_idf:
            for word, score in doc:
                tf_idf_saliency[word] += score / len(corpus_tf_idf)
        dictionary_with_tf_idf: Dict[str, float] = {}
        for i in range(len(tf_idf_saliency)):
            dictionary_with_tf_idf[dictionary[i]] = tf_idf_saliency[i]
        keys, values = sort(dictionary_with_tf_idf)
        return keys, values


def sort(dictionary: dict):
    keys = []
    values = []
    sort_dictionary = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
    for key, value in sort_dictionary:
        values.append(round(value, 4))
        keys.append(key)
    return keys, values

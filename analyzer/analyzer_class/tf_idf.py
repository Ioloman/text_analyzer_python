from collections import Counter
from gensim import corpora, models
import matplotlib.pyplot as plt
import numpy as np


class TFIDF(object):
    def __call__(self, texts):
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        tf_idf = models.TfidfModel(corpus)
        corpus_tf_idf = tf_idf[corpus]
        tf_idf_saliency = Counter()
        for doc in corpus_tf_idf:
            for word, score in doc:
                tf_idf_saliency[word] += score / len(corpus_tf_idf)
        dictionary_with_tf_idf = {}
        for i in range(len(tf_idf_saliency)):
            dictionary_with_tf_idf[dictionary[i]] = tf_idf_saliency[i]
        keys, values = sort(dictionary_with_tf_idf)
        return keys, values


def sort(dictionary):
    keys = []
    values = []
    sort_dictionary = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
    for key, value in sort_dictionary:
        values.append(round(value, 4))
        keys.append(key)
    return keys, values


def sum_tf_idf(tf_idf_dictionary_list):
    result_dictionary = {}  # результирующий словарь
    for dictionary in tf_idf_dictionary_list:  # пробегаем по списку словарей
        for key in dictionary:  # пробегаем по ключам словаря
            try:
                result_dictionary[key] += dictionary[key]  # складываем значения
            except KeyError:  # если ключа еще нет - создаем
                result_dictionary[key] = dictionary[key]

    return result_dictionary


def graphik(keys, values):
    lag = 1
    x = np.arange(0, len(keys), lag)
    y = values
    fig = plt.figure()
    plt.plot(x, y)
    plt.show()

import math
from collections import Counter
from typing import List, Tuple, Dict
from functools import reduce


def compute_tf(corpus: List[List[str]]) -> Dict[str, float]:
    tf_dict = Counter(reduce(lambda a, b: a + b, corpus))
    for word in tf_dict:
        tf_dict[word] /= len(tf_dict)

    return tf_dict


def compute_idf(word: str, corpus: List[List[str]]) -> float:
    return math.log10(len(corpus) / sum([1 for text in corpus if word in text]))


def compute_tfidf(corpus: List[List[str]]) -> Tuple[List[str], List[float]]:
    tfidf_dict = compute_tf(corpus)
    for word in tfidf_dict:
        tfidf_dict[word] *= compute_idf(word, corpus)
    return sort(tfidf_dict)


def sort(dictionary: dict):
    keys = []
    values = []
    sort_dictionary = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
    for key, value in sort_dictionary:
        values.append(round(value, 4))
        keys.append(key)
    return keys, values
